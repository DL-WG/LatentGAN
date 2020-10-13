###### Nadam Algorithm ######
## author: Jiaming Liu
## library: PyTorch
## year: 2017
## commit = adc49f2d4f448ecf6f08d7c7fdb0a0470d2a75de
## url = https://github.com/Jiaming-Liu/pytorch/blob/adc49f2d4f448ecf6f08d7c7fdb0a0470d2a75de/torch/optim/nadam.py 

import math
from torch.optim.optimizer import Optimizer

class Nadam(Optimizer):
    """Implements Nadam algorithm.
    It has been proposed in `Incorporating Nesterov Momentum into Adam`_.
    Arguments:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float, optional): learning rate (default: 2e-3)
        betas (Tuple[float, float], optional): coefficients used for computing
            running averages of gradient and its square (default: (0.975, 0.999))
        eps (float, optional): term added to the denominator to improve
            numerical stability (default: 1e-8)
        schedule_decay (float, optional): beta1 decay factor (default: 0)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
    .. _Incorporating Nesterov Momentum into Adam
        https://openreview.net/pdf?id=OM0jvwB8jIp57ZJjtNEZ
    """

    def __init__(self, params, lr=2e-3, betas=(0.975, 0.999), eps=1e-8,
                 schedule_decay=0, weight_decay=0):
        defaults = dict(lr=lr, betas=betas, eps=eps,
                        schedule_decay=schedule_decay, weight_decay=weight_decay,
                        prod_beta1=1.)
        super(Nadam, self).__init__(params, defaults)

    def step(self, closure=None):
        """Performs a single optimization step.
        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            beta1, beta2 = group['betas']

            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad.data
                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state['step'] = 0
                    # Exponential moving average of gradient values
                    state['exp_avg'] = grad.new().resize_as_(grad).zero_()
                    # Exponential moving average of squared gradient values
                    state['exp_avg_sq'] = grad.new().resize_as_(grad).zero_()

                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                state['step'] += 1

                if group['weight_decay'] != 0:
                    grad = grad.add(group['weight_decay'], p.data)

                schedule_decay = group['schedule_decay']
                cur_beta1 = beta1 * (1. - 0.5 * (0.96 ** (state['step'] * schedule_decay)))
                next_beta1 = beta1 * (1. - 0.5 * (0.96 ** ((state['step'] + 1) * schedule_decay)))
                prod_beta1 = group['prod_beta1']
                prod_beta1 *= cur_beta1
                next_prod_beta1 = prod_beta1 * next_beta1
                bias_correction1 = (1 - cur_beta1) / (1 - prod_beta1)
                next_bias_correction1 = next_beta1 / (1 - next_prod_beta1)

                # Decay the first and second moment running average coefficient
                exp_avg.mul_(cur_beta1).add_(1 - cur_beta1, grad)
                exp_avg_sq.mul_(beta2).addcmul_(1 - beta2, grad, grad)

                sqrt_bias_correction2 = math.sqrt((1 - beta2 ** state['step']) / beta2)
                step_size = group['lr'] * sqrt_bias_correction2

                denom = exp_avg_sq.sqrt().add_(group['eps'])

                # For memory efficiency, separate update into two
                p.data.addcdiv_(-step_size * next_bias_correction1, exp_avg, denom)
                p.data.addcdiv_(-step_size * bias_correction1, grad, denom)

                # update prod_beta1
                group['prod_beta1'] = prod_beta1

        return loss
import numpy as np
from scipy.sparse import coo_matrix


class Constraints2D:
    r"""
    Local (sparse) constraints to apply to the spline part of the salt model.
    The SED model is defined as :

     .. math::
        S(\lambda, t) = X_0 [M_0(\lambda, p) + X_1 M_1(\lambda, p)] \, e^{CL(\lambda) \, C}

    where the 2D surfaces are defined on the same spline basis :

    .. math::
        M_{0|1}(\lambda, \mathrm{p}) = \sum_{k\ell} \theta_{k\ell}^{0|1} \mathcal{B}^t_k(\mathrm{p})
        \mathcal{B}^m_l(\mathrm{\lambda})

    Constraints are:

    .. math::
        \int M_0(\lambda, p = 0, ) T_B(\lambda) \frac{\lambda}{hc} d\lambda = 1 \\

         \int M_1(\lambda, p = 0, ) T_B(\lambda) \frac{\lambda}{hc} d\lambda = 1 \\

        \int \left.\frac{\partial M_0(\lambda, p = 0)}{\partial t}\right|_{t = t_{max}^{B^\star}}
        T_B(\lambda) \frac{\lambda}{hc} d\lambda = 0 \\

         \int \left.\frac{\partial M_1(\lambda, p = 0)}{\partial t}\right|_{t = t_{max}^{B^\star}}
         T_B(\lambda) \frac{\lambda}{hc} d\lambda = 0 \\

         \left<c\right> = 0 \\

         \left<X_1\right> = 0 \\

         \left<(X_1 - \left<X_1\right>)^2\right> = 1 \\

    Six first constraints are linear. They are implemented in the same form :

    .. math::
        C(\beta) =  \alpha - H_{pen} \beta

    For practical reasons, :math:`H_{pen}` and :math:`\alpha` are divided by the square root of the constraints
    quadratic penalty, :math:`\sigma_{pen} = \sqrt{\mu_{pen}}`

    The last one is a quadratic constraint then it is called : :math:`C^1(X_1)`
    Only the constraint involving the free parameters of the model are considered.

    Attributes
    ----------
    model : nacl.salt
        Model.
    pars : nacl.lib.fitparameters
        Model parameters.
    basis : nacl.lib.bspline
        Model basis 2D surfaces splines 2D basis (wavelength, phase)

    parameters_cons : list
        Free parameters of the model, parameters to constraints

    x1_var_real : bool
        If False, consider that the mean of the constraint on the :math:`X_1` is already true, which mean that

         .. math::
             C^1(X_1) = \left<(X_1)^2\right> = 1

        If True :

         .. math::
             C^1(X_1) = \left<(X_1 - \left<X_1\right>)^2\right> = 1

    vals : array
         Values of the :math:`\alpha` vector, divided by :math:`\sigma_{pen}`

    sig_vals : array
        Values of the :math:`\sigma_{pen}` vector.

    mu_pq : float
        Values of the linear constraint quadratic penalty amplitude.
    mu_pq_var_x1 :
        Values of the :math:`X_1` variance constraint quadratic penalty amplitude.

    H : scipy.sparse.coo_matrix
        :math:`H_{pen}` divided by the square root of the constraints quadratic penalty, :math:`\sigma_{pen}`
    """

    def __init__(self, model, mu_pq, parameters_cons=['M0', 'X0', 'tmax'],
                 mu_pq_var_x1=None, x1_var_real=False):
        r"""
        Constructor.
        Creation of the sparse matrix :math:`H_{pen}`.
        Since the constraints are linear, each line correspond to a constraint and the colon to the model parameters
        (: :math:`\beta`) involved in this constraint.

        Parameters
        ----------
        model : nacl.salt
            Model.
        mu_pq : float
            Values of the linear constraint quadratic penalty amplitude.
        parameters_cons : list
            Free parameters of the model, parameters to constraints
        mu_pq_var_x1 :
            Values of the :math:`X_1` variance constraint quadratic penalty amplitude.
        x1_var_real : bool
            If False, consider that the mean of the constraint on the :math:`X_1` is already true, which mean that

             .. math::
                 C^1(X_1) = \left< (X_1)^2 \right> = 1

            If True :

             .. math::
                 C^1(X_1) = \left< (X_1 - \left< X_1 \right> )^2 \right> = 1
        """
        self.model = model
        self.parameters_cons = parameters_cons
        self.x1_var_real = x1_var_real
        
        self.pars = self.model.pars
        self.basis = self.model.basis

        n = len(self.pars.full)
        pp = self.pars.copy()
        pp.release()
        nsn = len(pp['X0'].full)
        self.vals = []  # vals
        tr = self.model.filter_db.transmission_db['SWOPE::B']
        tr_eval, _ = self.model.filter_db.insert(tr, z=0)
        filter_z = self.model.gram.dot(tr_eval)
        comp_t = 0
        self.mu_pq = mu_pq
        if mu_pq_var_x1 is None:
            self.mu_pq_var_x1 = self.mu_pq
        else:
            self.mu_pq_var_x1 = mu_pq_var_x1
        sigma = 1/np.sqrt(self.mu_pq)
        self.sig_vals = []
        
        i = np.array([])
        j = np.array([])
        v = np.array([])
        
        if ('M0' in parameters_cons) & ('X0' in parameters_cons):
            # first constraint: S(phase = 0, band = B) == 1.
            surface0_eval = self.model.basis.by.eval(np.array([0.])).toarray()
            jacobian = coo_matrix(np.outer(surface0_eval, filter_z).ravel())
            i = np.hstack((i, pp['M0'].indexof(jacobian.col)))
            j = np.hstack((j, np.full(len(jacobian.col), comp_t)))
            v = np.hstack((v, jacobian.data.copy()))
            comp_t += 1
            self.vals.append(1)
            self.sig_vals.append(sigma)
            
        if ('M0' in parameters_cons) & ('tmax' in parameters_cons):
            # second constraint: S'(phase = 0) == 0. band = B
            surface_zero_derivative = self.model.basis.by.deriv(np.array([0.])).toarray()
            integral_zero_derivative = coo_matrix(np.outer(surface_zero_derivative, filter_z).ravel())
            i = np.hstack((i, pp['M0'].indexof(integral_zero_derivative.col)))
            j = np.hstack((j, np.full(len(integral_zero_derivative.col), comp_t)))
            v = np.hstack((v, integral_zero_derivative.data.copy()))
            comp_t += 1
            self.vals.append(0)
            self.sig_vals.append(sigma)
            
        if ('M1' in parameters_cons) & ('X1' in parameters_cons):
            # third constraint: flux_broadband_max  = 0
            surface1_eval = self.model.basis.by.eval(np.array([0.])).toarray()
            jacobian = coo_matrix(np.outer(surface1_eval, filter_z).ravel())
            i = np.hstack((i, pp['M1'].indexof(jacobian.col)))
            j = np.hstack((j, np.full(len(jacobian.col), comp_t)))
            v = np.hstack((v, jacobian.data.copy()))
            comp_t += 1
            self.vals.append(0)
            self.sig_vals.append(sigma)
                       
        if ('M1' in parameters_cons) & ('tmax' in parameters_cons):
            # fourth constraint: flux_broadband_max = 0
            surface1_zero_derivative = self.model.basis.by.deriv(np.array([0.])).toarray()
            integral1_zero_derivative = coo_matrix(np.outer(surface1_zero_derivative, filter_z).ravel())
            i = np.hstack((i, pp['M1'].indexof(integral1_zero_derivative.col)))
            j = np.hstack((j, np.full(len(integral1_zero_derivative.col), comp_t)))
            v = np.hstack((v, integral1_zero_derivative.data.copy()))
            comp_t += 1
            self.vals.append(0)
            self.sig_vals.append(sigma)
           
        v *= self.model.norm
        
        if 'X1' in parameters_cons:            
            # mean X1 = 0
            i = np.hstack((i, pp['X1'].indexof(np.arange(nsn))))
            j = np.hstack((j, np.full(nsn, comp_t)))
            v = np.hstack((v, np.full(nsn, 1)))  # X1 new constraint 1e-5
            comp_t += 1
            self.vals.append(0)
            self.sig_vals.append(sigma)
           
        if 'c' in parameters_cons:
            # mean c = 0
            i = np.hstack((i, pp['c'].indexof(np.arange(nsn))))
            j = np.hstack((j, np.full(nsn, comp_t)))
            v = np.hstack((v, np.full(nsn, 1)))
            comp_t += 1
            self.vals.append(0)
            self.sig_vals.append(sigma)

        self.cl_i = None
        self.sig_vals = np.array(self.sig_vals)
        self.vals = np.array(self.vals)/self.sig_vals
        v /= self.sig_vals[np.array(j).astype(int)]
        
        self.H = coo_matrix((v, (i, j)), shape=(n, len(self.vals))).tocsr()

        if 'X1' in self.parameters_cons:
            self.var_x1 = self.var_x1
        else:
            self.var_x1 = None
            
    def var_x1(self, beta, gamma=[], jac=False):
        r"""
        Evaluate the seventh constraints, on the variance of the :math:`X_1` parameters.

        If the attributes x1_var_real is True, then compute :
            the constraint :

            .. math::
                 C^1(X_1) = \left<(X_1 - \left<X_1\right>)^2\right> = 1

            it firsts derivatives wrt :math:`X_1` :

            .. math::
                \frac{dC(X_1)}{dX_1^i} = \frac{2}{N} (X_1 - \bar{X_1})^T \left(\begin{matrix}
                - \frac{1}{N} \\
                ... \\
                (1 - \frac{1}{N})_i \\
                ... \\
                - \frac{1}{N}
                \end{matrix} \right)

            it seconds derivatives wrt :math:`X_1` :

                .. math::
                    \frac{d^2C(X_1)}{dX_1^j dX_1^i} &= \frac{2}{N} \left(\begin{matrix}
                    - \frac{1}{N} \\
                    ... \\
                    (1 - \frac{1}{N})_j \\
                    ... \\
                    - \frac{1}{N}
                    \end{matrix} \right)^T  \left(\begin{matrix}
                    - \frac{1}{N} \\
                    ... \\
                    (1 - \frac{1}{N})_i \\
                    ... \\
                    - \frac{1}{N}
                    \end{matrix} \right)

        If the attributes x1_var_real is False :

        .. math::
            C^1(X_1) =  \frac{1}{N} X_1^T X_1 \quad  \& \quad
            \frac{\partial C^1(X_1)}{\partial X_1^i} = \frac{2}{N^2} X_1^T  \quad  \& \quad
            \frac{\partial^2 C^1(X_1)}{ \partial X_1^j \partial X_1^i} = \frac{2}{N^2} \delta{ij}


        Parameters
        ----------
        beta : array
            Model parameters.
        gamma : array
            Variance model parameters.
        jac : bool
            If derivatives are needed.

        Returns
        -------
        cons : array
            Value of the constraints multiply by the square root of mu_pq_var_x1

        if jac is True :
        jacobian_cons : array
            Gradient of the constraints multiply by mu_pq_var_x1
        hessian_cons :
            Hessian of the constraints multiply by mu_pq_var_x1
        """

        self.pars.free = beta
        pp = self.pars.copy()
        nsn = len(pp['X1'].full)
        diag = np.zeros_like(pp.free)
        i = pp['X1'].indexof(np.arange(nsn))
        xh, yh = np.meshgrid(i, i)
        if self.x1_var_real is False:
            diag[i] = np.ones(nsn)
            cons = pp['X1'].free.var() - 1
            dc0 = 2/nsn * diag * pp.free
            dc = np.matrix(dc0[i])
            jacobian_cons = 2 * dc0 * cons
            # if gamma is not None:
            # jacobian_cons = self.mu_pq * np.hstack((jacobian_cons, np.zeros(len(gamma))))
            jacobian_cons = self.mu_pq_var_x1 * np.hstack((jacobian_cons, np.zeros(len(gamma))))
            hh = np.diag([2/nsn] * len(i))
            # hessian_cons = self.mu_pq * (2 * np.matrix(hh) * cons + 2 * dc.T @ dc)
            hessian_cons = self.mu_pq_var_x1 * (2 * np.matrix(hh) * cons + 2 * dc.T @ dc)

        # ## new implementation
        # ## here mean is not Zero, mush longer for the fit to
        # ## reach the constraints but when we start far from
        # ## <X1> != 0 needed
        elif self.x1_var_real:
            jacobian_cons = np.zeros_like(pp.free)
            x1mean = pp['X1'].free.mean()
            x1v = pp['X1'].free - x1mean
            cons = pp['X1'].free.var() - 1  # np.mean(x1v**2) - 1

            dc_dxi = 2 / nsn ** 2 * (nsn * pp['X1'].free - (2 * nsn - 1) * x1mean)
            jacobian_cons[i] = 2 * cons * dc_dxi
            jacobian_cons = self.mu_pq_var_x1 * np.hstack((jacobian_cons, np.zeros(len(gamma))))

            dc_dxi_2 = 2 / nsn ** 2 * (nsn * np.diag(np.ones_like(x1v)) - (2 * nsn - 1) / nsn)
            hessian_cons = self.mu_pq_var_x1 * 2 * (dc_dxi.reshape(-1, 1) @ dc_dxi.reshape(-1, 1).T + cons * dc_dxi_2)

        idx = (yh.ravel() != -1) & (xh.ravel() != -1)
        hessian_cons = coo_matrix((np.array(hessian_cons).ravel()[idx],
                                   (yh.ravel()[idx], xh.ravel()[idx])),
                                  shape=(len(pp.free)+len(gamma), len(pp.free)+len(gamma)))
        cons *= np.sqrt(self.mu_pq_var_x1)
        if jac:
            return cons, jacobian_cons, hessian_cons
        return cons

    def get_rhs(self):
        i = np.where(self.pars.indexof() >= 0)[0]
        h = self.H[i, :].tocoo()
        idx = np.bincount(h.col, minlength=len(self.vals)) > 0
        return self.vals[idx]

    def __call__(self, beta, jac=False):
        r"""
        Evaluate the linear constraints: :math:`C(\beta) = \alpha - H_{pen} \beta`

        Parameters
        ----------
        beta : array
            Model parameters.
        jac : bool
            If derivatives are needed.

        Returns
        -------
        v : array
            Value of the constraints multiply by the square root of :math:`\mu_{pq}`
        if jac is True :
        h : array
            Matrix :math:`H_{pen}` by :math:`\mu_{pq}`
        """
        self.pars.free = beta            
        v = -self.H.T @ self.pars.full + self.vals
        # we need to evaluate how many constraints are still valid,
        # given which parameters are fixed. We do that by slicing the
        # constraint matrix. There is probably a better and faster
        # way, which avoids having to do this each time the
        # constraints are evaluated
        i = np.where(self.pars.indexof() >= 0)[0]
        h = self.H[i, :].tocoo()
        # verify that all columns of H are populated
        j = np.where(np.bincount(h.col) > 0)[0]
        h = h.tocsr()[:, j].tocoo()
        # we need also to slice the return values
        idx = np.bincount(h.col, minlength=len(self.vals)) > 0
        if jac == 1:
            return v[idx], h.T
        return v[idx]

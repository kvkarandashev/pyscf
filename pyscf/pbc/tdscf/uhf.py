#!/usr/bin/env python
# Copyright 2014-2018 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

from pyscf import lib
from pyscf.tdscf import uhf


class TDA(uhf.TDA):
<<<<<<< HEAD

    conv_tol = getattr(__config__, 'pbc_tdscf_rhf_TDA_conv_tol', 1e-6)

    def __init__(self, mf):
        from pyscf.pbc import scf
        assert(isinstance(mf, scf.khf.KSCF))
        self.cell = mf.cell
        uhf.TDA.__init__(self, mf)
        from pyscf.pbc.df.df_ao2mo import warn_pbc2d_eri
        warn_pbc2d_eri(mf)

    def get_vind(self, mf):
        '''Compute Ax'''
        singlet = self.singlet
        cell = mf.cell
        kpts = mf.kpts

        mo_coeff = mf.mo_coeff
        mo_energy = mf.mo_energy
        mo_occ = mf.mo_occ
        nkpts = len(mo_occ)
        nao, nmo = mo_coeff[0][0].shape
        occidxa = [numpy.where(mo_occ[0][k]> 0)[0] for k in range(nkpts)]
        occidxb = [numpy.where(mo_occ[1][k]> 0)[0] for k in range(nkpts)]
        viridxa = [numpy.where(mo_occ[0][k]==0)[0] for k in range(nkpts)]
        viridxb = [numpy.where(mo_occ[1][k]==0)[0] for k in range(nkpts)]
        orboa = [mo_coeff[0][k][:,occidxa[k]] for k in range(nkpts)]
        orbob = [mo_coeff[1][k][:,occidxb[k]] for k in range(nkpts)]
        orbva = [mo_coeff[0][k][:,viridxa[k]] for k in range(nkpts)]
        orbvb = [mo_coeff[1][k][:,viridxb[k]] for k in range(nkpts)]

        e_ia_a = _get_e_ia(mo_energy[0], mo_occ[0])
        e_ia_b = _get_e_ia(mo_energy[1], mo_occ[1])
        hdiag = numpy.hstack([x.ravel() for x in (e_ia_a + e_ia_b)])
        tot_x_a = sum(x.size for x in e_ia_a)
        tot_x_b = sum(x.size for x in e_ia_b)

        mem_now = lib.current_memory()[0]
        max_memory = max(2000, self.max_memory*.8-mem_now)
        vresp = _gen_uhf_response(mf, hermi=0, max_memory=max_memory)

        def vind(zs):
            nz = len(zs)
            zs = [_unpack(z, mo_occ) for z in zs]
            dmov = numpy.empty((2,nz,nkpts,nao,nao), dtype=numpy.complex128)
            for i in range(nz):
                dm1a, dm1b = zs[i]
                for k in range(nkpts):
                    dmov[0,i,k] = reduce(numpy.dot, (orboa[k], dm1a[k], orbva[k].conj().T))
                    dmov[1,i,k] = reduce(numpy.dot, (orbob[k], dm1b[k], orbvb[k].conj().T))

<<<<<<< HEAD
            with lib.temporary_env(mf, exxdiv=None):
                v1ao = vresp(dmvo)
=======
            dmov = dmov.reshape(2*nz,nkpts,nao,nao)
            v1ao = vresp(dmov)
            v1ao = v1ao.reshape(2,nz,nkpts,nao,nao)
>>>>>>> upstream/master
            v1s = []
            for i in range(nz):
                dm1a, dm1b = zs[i]
                v1as = []
                v1bs = []
                for k in range(nkpts):
                    v1a = reduce(numpy.dot, (orboa[k].conj().T, v1ao[0,i,k], orbva[k]))
                    v1b = reduce(numpy.dot, (orbob[k].conj().T, v1ao[1,i,k], orbvb[k]))
                    v1a += e_ia_a[k] * dm1a[k]
                    v1b += e_ia_b[k] * dm1b[k]
                    v1as.append(v1a.ravel())
                    v1bs.append(v1b.ravel())
                v1s += v1as + v1bs
            return numpy.hstack(v1s).reshape(nz,-1)
=======
    def gen_vind(self, mf):
        vind, hdiag = uhf.TDA.gen_vind(self, mf)
        def vindp(x):
            with lib.temporary_env(mf, exxdiv=None):
                return vind(x)
        return vindp, hdiag
>>>>>>> upstream/dev

    def nuc_grad_method(self):
        raise NotImplementedError

CIS = TDA


<<<<<<< HEAD
class TDHF(TDA):
    def get_vind(self, mf):
        singlet = self.singlet
        cell = mf.cell
        kpts = mf.kpts

        mo_coeff = mf.mo_coeff
        mo_energy = mf.mo_energy
        mo_occ = mf.mo_occ
        nkpts = len(mo_occ)
        nao, nmo = mo_coeff[0][0].shape
        occidxa = [numpy.where(mo_occ[0][k]> 0)[0] for k in range(nkpts)]
        occidxb = [numpy.where(mo_occ[1][k]> 0)[0] for k in range(nkpts)]
        viridxa = [numpy.where(mo_occ[0][k]==0)[0] for k in range(nkpts)]
        viridxb = [numpy.where(mo_occ[1][k]==0)[0] for k in range(nkpts)]
        orboa = [mo_coeff[0][k][:,occidxa[k]] for k in range(nkpts)]
        orbob = [mo_coeff[1][k][:,occidxb[k]] for k in range(nkpts)]
        orbva = [mo_coeff[0][k][:,viridxa[k]] for k in range(nkpts)]
        orbvb = [mo_coeff[1][k][:,viridxb[k]] for k in range(nkpts)]

        e_ia_a = _get_e_ia(mo_energy[0], mo_occ[0])
        e_ia_b = _get_e_ia(mo_energy[1], mo_occ[1])
        hdiag = numpy.hstack([x.ravel() for x in (e_ia_a + e_ia_b)])
        hdiag = numpy.hstack((hdiag, hdiag))
        tot_x_a = sum(x.size for x in e_ia_a)
        tot_x_b = sum(x.size for x in e_ia_b)
        tot_x = tot_x_a + tot_x_b

        mem_now = lib.current_memory()[0]
        max_memory = max(2000, self.max_memory*.8-mem_now)
        vresp = _gen_uhf_response(mf, hermi=0, max_memory=max_memory)

        def vind(xys):
            nz = len(xys)
            x1s = [_unpack(x[:tot_x], mo_occ) for x in xys]
            y1s = [_unpack(x[tot_x:], mo_occ) for x in xys]
            dmov = numpy.empty((2,nz,nkpts,nao,nao), dtype=numpy.complex128)
            for i in range(nz):
                xa, xb = x1s[i]
                ya, yb = y1s[i]
                for k in range(nkpts):
<<<<<<< HEAD
                    dmx = reduce(numpy.dot, (orbva[k], xa[k], orboa[k].T.conj()))
                    dmy = reduce(numpy.dot, (orboa[k], ya[k].T, orbva[k].T.conj()))
                    dmvo[0,i,k] = dmx + dmy  # AX + BY
                    dmx = reduce(numpy.dot, (orbvb[k], xb[k], orbob[k].T.conj()))
                    dmy = reduce(numpy.dot, (orbob[k], yb[k].T, orbvb[k].T.conj()))
                    dmvo[1,i,k] = dmx + dmy  # AX + BY

            with lib.temporary_env(mf, exxdiv=None):
                v1ao = vresp(dmvo)
=======
                    dmx = reduce(numpy.dot, (orboa[k], xa[k]  , orbva[k].conj().T))
                    dmy = reduce(numpy.dot, (orbva[k], ya[k].T, orboa[k].conj().T))
                    dmov[0,i,k] = dmx + dmy  # AX + BY
                    dmx = reduce(numpy.dot, (orbob[k], xb[k]  , orbvb[k].conj().T))
                    dmy = reduce(numpy.dot, (orbvb[k], yb[k].T, orbob[k].conj().T))
                    dmov[1,i,k] = dmx + dmy  # AX + BY

            dmov = dmov.reshape(2*nz,nkpts,nao,nao)
            v1ao = vresp(dmov)
            v1ao = v1ao.reshape(2,nz,nkpts,nao,nao)
>>>>>>> upstream/master
            v1s = []
            for i in range(nz):
                xa, xb = x1s[i]
                ya, yb = y1s[i]
                v1xsa = []
                v1xsb = []
                v1ysa = []
                v1ysb = []
                for k in range(nkpts):
                    v1xa = reduce(numpy.dot, (orboa[k].conj().T, v1ao[0,i,k], orbva[k]))
                    v1xb = reduce(numpy.dot, (orbob[k].conj().T, v1ao[1,i,k], orbvb[k]))
                    v1ya = reduce(numpy.dot, (orbva[k].conj().T, v1ao[0,i,k], orboa[k])).T
                    v1yb = reduce(numpy.dot, (orbvb[k].conj().T, v1ao[1,i,k], orbob[k])).T
                    v1xa+= e_ia_a[k] * xa[k]
                    v1xb+= e_ia_b[k] * xb[k]
                    v1ya+= e_ia_a[k] * ya[k]
                    v1yb+= e_ia_b[k] * yb[k]
                    v1xsa.append(v1xa.ravel())
                    v1xsb.append(v1xb.ravel())
                    v1ysa.append(-v1ya.ravel())
                    v1ysb.append(-v1yb.ravel())
                v1s += v1xsa + v1xsb + v1ysa + v1ysb
            return numpy.hstack(v1s).reshape(nz,-1)

        return vind, hdiag

    def init_guess(self, mf, nstates=None, wfnsym=None):
        x0 = TDA.init_guess(self, mf, nstates)
        y0 = numpy.zeros_like(x0)
        return numpy.hstack((x0,y0))

    def kernel(self, x0=None):
        '''TDHF diagonalization with non-Hermitian eigenvalue solver
        '''
        self.check_sanity()
        self.dump_flags()

        vind, hdiag = self.get_vind(self._scf)
        precond = self.get_precond(hdiag)
        if x0 is None:
            x0 = self.init_guess(self._scf, self.nstates)
=======
class TDHF(uhf.TDHF):
    def gen_vind(self, mf):
        vind, hdiag = uhf.TDHF.gen_vind(self, mf)
        def vindp(x):
            with lib.temporary_env(mf, exxdiv=None):
                return vind(x)
        return vindp, hdiag
>>>>>>> upstream/dev

    def nuc_grad_method(self):
        raise NotImplementedError


RPA = TDUHF = TDHF



if __name__ == '__main__':
    from pyscf import gto
    from pyscf import scf
    mol = gto.Mole()
    mol.verbose = 0
    mol.output = None

    mol.atom = [
        ['H' , (0. , 0. , .917)],
        ['F' , (0. , 0. , 0.)], ]
    mol.basis = '631g'
    mol.build()

    mf = scf.UHF(mol).run()
    td = TDA(mf)
    td.nstates = 5
    td.verbose = 3
    print(td.kernel()[0] * 27.2114)
# [ 11.01748568  11.01748568  11.90277134  11.90277134  13.16955369]

    td = TDHF(mf)
    td.nstates = 5
    td.verbose = 3
    print(td.kernel()[0] * 27.2114)
# [ 10.89192986  10.89192986  11.83487865  11.83487865  12.6344099 ]

    mol.spin = 2
    mf = scf.UHF(mol).run()
    td = TDA(mf)
    td.nstates = 6
    td.verbose = 3
    print(td.kernel()[0] * 27.2114)
# FIXME:  first state
# [ 0.02231607274  3.32113736  18.55977052  21.01474222  21.61501962  25.0938973 ]

    td = TDHF(mf)
    td.nstates = 4
    td.verbose = 3
    print(td.kernel()[0] * 27.2114)
# [ 3.31267103  18.4954748   20.84935404  21.54808392]


from cosmoTransitions import generic_potential
from cosmoTransitions import transitionFinder as tf
from cosmoTransitions import pathDeformation as pd
import numpy as np


class A4_vev1(generic_potential.generic_potential):
    def init(self,Mn1=10.,Mn2=20.,Mch1=5.,Mch2=6.,Mh=125.10,mZ = 91.1876,mW = 80.379,mtop = 172.76,mbot = 4.18,mtau = 1.77686, mcharm = 1.27, mstrange = 0.093, mmuon = 0.1056583745, mup = 0.00216, mdown = 0.00467, melectron = 0.0005109989461, vh = 246.22):
        # SU(2)_L and U(1)_Y couplings
        self.mW = mW
        self.mZ = mZ
        self.vh = vh

        gl = 2*self.mW/self.vh
        gy = 2*np.sqrt(self.mZ**2 - self.mW**2)/self.vh
        
        self.Ndim = 5 # Number of dynamic classical fields. 1 real field + 2 complex fields -> 5 real fields 
        self.renormScaleSq = float(self.vh**2) # Renormalisation scale
        
        if ((6.*(float(Mn1)**2 - float(Mn2)**2)/(self.vh**2))**2 - 12*(2.*np.sqrt(3)*(float(Mch1)**2 - float(Mch2)**2)/(self.vh**2))**2 >0. ): #Check if masses are allowed
            self.Mn1 = float(Mn1)
            self.Mn2 = float(Mn2)
            self.Mch1 = float(Mch1)
            self.Mch2 = float(Mch2) 
        else:
            self.Mn1 = 0.
            self.Mn2 = 0.
            self.Mch1 = 0.
            self.Mch2 = 0.
        
        #Calculate constants from masses
        self.M0 = np.sqrt(3)/2.*Mh**2
        self.L1 = -(self.Mch1**2 + self.Mch2**2)/(self.vh**2)
        self.L4 = 2.*np.sqrt(3)*(self.Mch1**2 - self.Mch2**2)/(self.vh**2)
        self.L0 = np.sqrt(3)*self.M0/(self.vh**2) - self.L1
        xc1 = 6.*(self.Mn1**2 + self.Mn2**2)/(self.vh**2) + 5*self.L1
        xc2 = np.sqrt((6.*(self.Mn1**2 - self.Mn2**2)/(self.vh**2))**2 - 12*self.L4**2)
        self.L2 = 1/6.*(xc1 + xc2 + self.L1)
        self.L3 = 1/4.*(xc1 - xc2 - self.L1)

        self.dM0 = 0
        self.dL0 = 0
        self.dL1 = 0
        self.dL2 = 0
        self.dL3 = 0
        self.dL4 = 0
        
        # Yukawa Couplings
        self.yt   = np.sqrt(2)*mtop/self.vh
        self.yb   = np.sqrt(2)*mbot/self.vh
        self.ytau = np.sqrt(2)*mtau/self.vh
        self.yc   = np.sqrt(2)*mcharm/self.vh
        self.ys   = np.sqrt(2)*mstrange/self.vh
        self.ymuon = np.sqrt(2)*mmuon/self.vh 
        self.yu   = np.sqrt(2)*mup/self.vh
        self.yd   = np.sqrt(2)*mdown/self.vh
        self.ye = np.sqrt(2)*melectron/self.vh     

        # Daisy thermal loop corrections
        self.cT = (14./3.*self.L0 + self.L1 + self.L2 + 2./3.*self.L3 + 3./2.*gl**2 + 3./4.*(gl**2 + gy**2) + 3.*(self.yt**2 + self.yb**2 + self.yc**2 + self.ys**2 + self.yu**2 + self.yd**2) + (self.ytau**2 + self.ymuon**2 + self.ye**2))/24.

        # Counterterms: Apply the renormalization conditions both to fix the minimum of the potential and the masses (first and second derivatives)
        tl_vevs = np.array([self.vh/np.sqrt(3), self.vh/np.sqrt(3), 0., self.vh/np.sqrt(3), 0.]) # Set VEVs at T=0
        gradT0 = self.gradV(tl_vevs,0.) # Take the first derivatives of the potential at the minimum
        Hess = self.d2V(tl_vevs,0.) # Use built-in d2V function to extrac the second derivative of the T=0 potential (tree + CW)        
        Hess_tree = self.massSqMatrix(tl_vevs) # Use analytical form of mass matrix in the gauge eigenbasis in the minimum
        d2V_CW = Hess - Hess_tree # Extrac the second derivative of the CW potential by removing the tree-level part from the full tree+CW T=0 bit 

        self.dM0 = float(np.sqrt(3)*(3/2 * 1/tl_vevs[0] * gradT0[0] - 1/2 * d2V_CW[0,0] - d2V_CW[1,0]))
        self.dL0 = float(3/2 * (1/(tl_vevs[0]**3) * gradT0[0] - 1/(tl_vevs[0]**2) * d2V_CW[0,0]))
        self.dL1 = float(-1/(tl_vevs[0]**3) * gradT0[0] + 1/(tl_vevs[0]**2) * (d2V_CW[0,0] - d2V_CW[1,0]))
        self.dL2 = float(-1/(tl_vevs[0]**3) * gradT0[0] + 1/(tl_vevs[0]**2) * (d2V_CW[0,0] - d2V_CW[1,0] + 2 * d2V_CW[4,2]))
        self.dL4 = float(-2/(tl_vevs[0]**2) * d2V_CW[2,0])
        
        # Printing Constants, Counterterms, VEVs at T=0 and Days thermal loop corrections
        print("M0 = ", self.M0)
        print("L0 = ", self.L0)
        print("L1 = ", self.L1)
        print("L2 = ", self.L2)
        print("L3 = ", self.L3)
        print("L4 = ", self.L4)
        print("dM0 = ", self.dM0)
        print("dL0 = ", self.dL0)
        print("dL1 = ", self.dL1)
        print("dL2 = ", self.dL2)
        print("dL3 = ", self.dL3)
        print("dL4 = ", self.dL4)
        print("Re(v1) =",tl_vevs[0])
        #print("Im(v1) =",tl_vevs[1])
        print("Re(v2) =",tl_vevs[1])
        print("Im(v2) =",tl_vevs[2])
        print("Re(v3) =",tl_vevs[3])
        print("Im(v3) =",tl_vevs[4])
        print("cT :", self.cT)

    def tree_lvl_conditions(self):
        # Here cond=true means that one is in the physical region at tree level
        req1 = self.M0 > 0
        req2 = self.L0 + self.L1 >0
        req3 = self.L4**2 < 12*self.L1**2
        req4 = self.L4**2 < 2*(self.L3 - self.L1)*(self.L2 - self.L1)
        
        cond = req1 and req2 and req3 and req4
        print("CONDITIONS : ", cond)

        return([req1,req2,req3,req4],cond)


    def forbidPhaseCrit(self, X):
        return (np.array([X])[...,0] < -1E-3).any()
        
    def V0(self, X):

        # A4 flavour symmetric potential with three SU(2) doublets
        # Each doublet has a complex VEV on the neutral component treated as a complex field
        # Each complex field will be treated as two real fields
        # Hi0 and Hi1 correspond to the real and complex parts resp.
        
        X = np.asanyarray(X)
        H10,H20,H21,H30,H31 = X[...,0], X[...,1], X[...,2], X[...,3], X[...,4]
        H11 = np.zeros_like(H10)

        r = -(self.M0+self.dM0)/(2.*np.sqrt(3.))*(H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)  \
        + 1/12.*(self.L0+self.dL0)*(H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)**2  \
        + 1/12.*(self.L3+self.dL3)*((H10**2 + H11**2)**2 + (H20**2 + H21**2)**2 + (H30**2 + H31**2)**2 - (H10**2 + H11**2)*(H20**2 + H21**2) - (H20**2 + H21**2)*(H30**2 + H31**2) - (H30**2 + H31**2)*(H10**2 + H11**2))  \
        + 1/4.*(self.L1+self.dL1)*(H10**2*H20**2 + H11**2*H21**2 + H20**2*H30**2 + H21**2*H31**2 +H30**2*H10**2 + H31**2*H11**2 + 2*H10*H11*H20*H21 + 2*H20*H21*H30*H31 + 2*H30*H31*H10*H11)  \
        + 1/4.*(self.L2+self.dL2)*(H10**2*H21**2 + H11**2*H20**2 + H20**2*H31**2 + H21**2*H30**2 +H30**2*H11**2 + H31**2*H10**2 - 2*H10*H11*H20*H21 - 2*H20*H21*H30*H31 - 2*H30*H31*H10*H11)  \
        + 1/4.*(self.L4+self.dL4)*(H10*H11*H21**2 - H10*H11*H20**2 + H20*H21*H31**2 - H20*H21*H30**2 + H30*H31*H11**2 - H30*H31*H10**2 - H20*H21*H11**2 + H20*H21*H10**2 - H30*H31*H21**2 + H30*H31*H20**2 - H10*H11*H31**2 + H10*H11*H30**2)

        return r

### Field-dependent masses are generic
# Calculations must be prepared to handle ndarrays as input
# X is a (..., Ndim) matrix containing multiple values for all dynamic fields
# The first axis correspond to the multiple values the fields may take
# The second axis correspond to the fields themselves
# M must be a (..., Nf) matrix where Nf is the number of field-dependent masses

    def boson_massSq(self, X, T):
        X = np.array(X) 
        H10,H20,H21,H30,H31 = X[...,0], X[...,1], X[...,2], X[...,3], X[...,4] # Extracting array containing multiple values for each individual field
        H11 = np.zeros_like(H10)
        
        # Scalar fields in gauge basis: H1, Eta1, Chi1, Chip1, H2, Eta2, Chi2, Chip2, H3, Eta3, Chi3, Chip3

        # Thermal correction do add on diagonal of mass matrices
        thcorr = np.full_like(H10, 2*self.cT*T**2)
        
        # C: charged component fields (Chi1, Chip1, Chi2, Chip2, Chi3, Chip3) mass matrix
        # Careful with 0 (zero) entries. Must be same type as other entries which maybe ndarrays of floats or complexs.
        # Use np.zeros_like(X[...,0]) to assure same type. 
        cm = np.array([[((2*H10**2 + 2*H11**2 + 2*(H20**2 + H21**2 + H30**2 + H31**2))*self.L0)/6. + ((2*H10**2 + 2*H11**2 - H20**2 - H21**2 - H30**2 - H31**2)*self.L3)/6. - self.M0/np.sqrt(3) + thcorr,\
                        np.zeros_like(H10),\
                        ((2*H10*H20 + 2*H11*H21)*self.L1)/4. + ((-(H11*H20) + H10*H21)*self.L4)/4.,\
                        ((-2*H11*H20 + 2*H10*H21)*self.L2)/4. + ((H10*H20 + H11*H21)*self.L4)/4.,\
                        ((2*H10*H30 + 2*H11*H31)*self.L1)/4. + ((H11*H30 - H10*H31)*self.L4)/4.,\
                        ((-2*H11*H30 + 2*H10*H31)*self.L2)/4. + ((-(H10*H30) - H11*H31)*self.L4)/4.],\
                       [np.zeros_like(H10),\
                        ((2*H10**2 + 2*H11**2 + 2*(H20**2 + H21**2 + H30**2 + H31**2))*self.L0)/6. + ((2*H10**2 + 2*H11**2 - H20**2 - H21**2 - H30**2 - H31**2)*self.L3)/6. - self.M0/np.sqrt(3) + thcorr,\
                        ((2*H11*H20 - 2*H10*H21)*self.L2)/4. + ((-(H10*H20) - H11*H21)*self.L4)/4.,\
                        ((2*H10*H20 + 2*H11*H21)*self.L1)/4. + ((-(H11*H20) + H10*H21)*self.L4)/4.,\
                        ((2*H11*H30 - 2*H10*H31)*self.L2)/4. + ((H10*H30 + H11*H31)*self.L4)/4.,\
                        ((2*H10*H30 + 2*H11*H31)*self.L1)/4. + ((H11*H30 - H10*H31)*self.L4)/4.],\
                       [((2*H10*H20 + 2*H11*H21)*self.L1)/4. + ((-(H11*H20) + H10*H21)*self.L4)/4.,\
                        ((2*H11*H20 - 2*H10*H21)*self.L2)/4. + ((-(H10*H20) - H11*H21)*self.L4)/4.,\
                        ((H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)*self.L0)/3. + ((-H10**2 - H11**2 + 2*H20**2 + 2*H21**2 - H30**2 - H31**2)*self.L3)/6. - self.M0/np.sqrt(3) + thcorr,\
                        np.zeros_like(H10),\
                        ((2*H20*H30 + 2*H21*H31)*self.L1)/4. + ((-(H21*H30) + H20*H31)*self.L4)/4.,\
                        ((-2*H21*H30 + 2*H20*H31)*self.L2)/4. + ((H20*H30 + H21*H31)*self.L4)/4.],\
                       [((-2*H11*H20 + 2*H10*H21)*self.L2)/4. + ((H10*H20 + H11*H21)*self.L4)/4.,\
                        ((2*H10*H20 + 2*H11*H21)*self.L1)/4. + ((-(H11*H20) + H10*H21)*self.L4)/4.,\
                        np.zeros_like(H10),\
                        ((H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)*self.L0)/3. + ((-H10**2 - H11**2 + 2*H20**2 + 2*H21**2 - H30**2 - H31**2)*self.L3)/6. - self.M0/np.sqrt(3) + thcorr,\
                        ((2*H21*H30 - 2*H20*H31)*self.L2)/4. + ((-(H20*H30) - H21*H31)*self.L4)/4.,\
                        ((2*H20*H30 + 2*H21*H31)*self.L1)/4. + ((-(H21*H30) + H20*H31)*self.L4)/4.],\
                       [((2*H10*H30 + 2*H11*H31)*self.L1)/4. + ((H11*H30 - H10*H31)*self.L4)/4.,\
                        ((2*H11*H30 - 2*H10*H31)*self.L2)/4. + ((H10*H30 + H11*H31)*self.L4)/4.,\
                        ((2*H20*H30 + 2*H21*H31)*self.L1)/4. + ((-(H21*H30) + H20*H31)*self.L4)/4.,\
                        ((2*H21*H30 - 2*H20*H31)*self.L2)/4. + ((-(H20*H30) - H21*H31)*self.L4)/4.,\
                        ((H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)*self.L0)/3. + ((-H10**2 - H11**2 - H20**2 - H21**2 + 2*(H30**2 + H31**2))*self.L3)/6. - self.M0/np.sqrt(3) + thcorr,\
                        np.zeros_like(H10)],\
                       [((-2*H11*H30 + 2*H10*H31)*self.L2)/4. + ((-(H10*H30) - H11*H31)*self.L4)/4.,\
                        ((2*H10*H30 + 2*H11*H31)*self.L1)/4. + ((H11*H30 - H10*H31)*self.L4)/4.,\
                        ((-2*H21*H30 + 2*H20*H31)*self.L2)/4. + ((H20*H30 + H21*H31)*self.L4)/4.,\
                        ((2*H20*H30 + 2*H21*H31)*self.L1)/4. + ((-(H21*H30) + H20*H31)*self.L4)/4.,\
                        np.zeros_like(H10),\
                        ((H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)*self.L0)/3. + ((-H10**2 - H11**2 - H20**2 - H21**2 + 2*(H30**2 + H31**2))*self.L3)/6. - self.M0/np.sqrt(3) + thcorr]])
     
        # N: neutral component fields (H1, Eta1, H2, Eta2, H3, Eta3) mass matrix
        nm = np.array([[((6*H10**2 + 2*H11**2 + 2*H20**2 + 2*H21**2 + 2*H30**2 + 2*H31**2)*self.L0)/6. + ((3*H20**2 + 3*H30**2)*self.L1)/6. + ((3*H21**2 + 3*H31**2)*self.L2)/6. + ((6*H10**2 + 2*H11**2 - H20**2 - H21**2 - H30**2 - H31**2)*self.L3)/6. + ((3*H20*H21 - 3*H30*H31)*self.L4)/6. - self.M0/np.sqrt(3) + thcorr, \
                        (2*H10*H11*self.L0)/3. + ((H20*H21 + H30*H31)*self.L1)/2. - ((H20*H21 + H30*H31)*self.L2)/2. + (2*H10*H11*self.L3)/3. + ((-H20**2 + H21**2 + H30**2 - H31**2)*self.L4)/4., \
                        (2*H10*H20*self.L0)/3. + ((6*H10*H20 + 3*H11*H21)*self.L1)/6. - (H11*H21*self.L2)/2. - (H10*H20*self.L3)/3. + ((-3*H11*H20 + 3*H10*H21)*self.L4)/6., \
                        (2*H10*H21*self.L0)/3. + (H11*H20*self.L1)/2. + ((-3*H11*H20 + 6*H10*H21)*self.L2)/6. - (H10*H21*self.L3)/3. + ((3*H10*H20 + 3*H11*H21)*self.L4)/6., \
                        (2*H10*H30*self.L0)/3. + ((6*H10*H30 + 3*H11*H31)*self.L1)/6. - (H11*H31*self.L2)/2. - (H10*H30*self.L3)/3. + ((3*H11*H30 - 3*H10*H31)*self.L4)/6., \
                        (2*H10*H31*self.L0)/3. + (H11*H30*self.L1)/2. + ((-3*H11*H30 + 6*H10*H31)*self.L2)/6. - (H10*H31*self.L3)/3. + ((-3*H10*H30 - 3*H11*H31)*self.L4)/6.], \
                       [(2*H10*H11*self.L0)/3. + ((H20*H21 + H30*H31)*self.L1)/2. - ((H20*H21 + H30*H31)*self.L2)/2. + (2*H10*H11*self.L3)/3. + ((-H20**2 + H21**2 + H30**2 - H31**2)*self.L4)/4., \
                        ((2*H10**2 + 6*H11**2 + 2*H20**2 + 2*H21**2 + 2*H30**2 + 2*H31**2)*self.L0)/6. + ((3*H21**2 + 3*H31**2)*self.L1)/6. + ((3*H20**2 + 3*H30**2)*self.L2)/6. + ((2*H10**2 + 6*H11**2 - H20**2 - H21**2 - H30**2 - H31**2)*self.L3)/6. + ((-3*H20*H21 + 3*H30*H31)*self.L4)/6. - self.M0/np.sqrt(3) + thcorr, \
                        (2*H11*H20*self.L0)/3. + (H10*H21*self.L1)/2. + ((6*H11*H20 - 3*H10*H21)*self.L2)/6. - (H11*H20*self.L3)/3. + ((-3*H10*H20 - 3*H11*H21)*self.L4)/6., \
                        (2*H11*H21*self.L0)/3. + ((3*H10*H20 + 6*H11*H21)*self.L1)/6. - (H10*H20*self.L2)/2. - (H11*H21*self.L3)/3. + ((-3*H11*H20 + 3*H10*H21)*self.L4)/6., \
                        (2*H11*H30*self.L0)/3. + (H10*H31*self.L1)/2. + ((6*H11*H30 - 3*H10*H31)*self.L2)/6. - (H11*H30*self.L3)/3. + ((3*H10*H30 + 3*H11*H31)*self.L4)/6., \
                        (2*H11*H31*self.L0)/3. + ((3*H10*H30 + 6*H11*H31)*self.L1)/6. - (H10*H30*self.L2)/2. - (H11*H31*self.L3)/3. + ((3*H11*H30 - 3*H10*H31)*self.L4)/6.], \
                       [(2*H10*H20*self.L0)/3. + ((6*H10*H20 + 3*H11*H21)*self.L1)/6. - (H11*H21*self.L2)/2. - (H10*H20*self.L3)/3. + ((-3*H11*H20 + 3*H10*H21)*self.L4)/6., \
                        (2*H11*H20*self.L0)/3. + (H10*H21*self.L1)/2. + ((6*H11*H20 - 3*H10*H21)*self.L2)/6. - (H11*H20*self.L3)/3. + ((-3*H10*H20 - 3*H11*H21)*self.L4)/6., \
                        ((2*H10**2 + 2*H11**2 + 6*H20**2 + 2*H21**2 + 2*H30**2 + 2*H31**2)*self.L0)/6. + ((3*H10**2 + 3*H30**2)*self.L1)/6. + ((3*H11**2 + 3*H31**2)*self.L2)/6. + ((-H10**2 - H11**2 + 6*H20**2 + 2*H21**2 - H30**2 - H31**2)*self.L3)/6. + ((-3*H10*H11 + 3*H30*H31)*self.L4)/6. - self.M0/np.sqrt(3) + thcorr, \
                        (2*H20*H21*self.L0)/3. + ((H10*H11 + H30*H31)*self.L1)/2. - ((H10*H11 + H30*H31)*self.L2)/2. + (2*H20*H21*self.L3)/3. + ((H10**2 - H11**2 - H30**2 + H31**2)*self.L4)/4., \
                        (2*H20*H30*self.L0)/3. + ((6*H20*H30 + 3*H21*H31)*self.L1)/6. - (H21*H31*self.L2)/2. - (H20*H30*self.L3)/3. + ((-3*H21*H30 + 3*H20*H31)*self.L4)/6., \
                        (2*H20*H31*self.L0)/3. + (H21*H30*self.L1)/2. + ((-3*H21*H30 + 6*H20*H31)*self.L2)/6. - (H20*H31*self.L3)/3. + ((3*H20*H30 + 3*H21*H31)*self.L4)/6.], \
                       [(2*H10*H21*self.L0)/3. + (H11*H20*self.L1)/2. + ((-3*H11*H20 + 6*H10*H21)*self.L2)/6. - (H10*H21*self.L3)/3. + ((3*H10*H20 + 3*H11*H21)*self.L4)/6., \
                        (2*H11*H21*self.L0)/3. + ((3*H10*H20 + 6*H11*H21)*self.L1)/6. - (H10*H20*self.L2)/2. - (H11*H21*self.L3)/3. + ((-3*H11*H20 + 3*H10*H21)*self.L4)/6., \
                        (2*H20*H21*self.L0)/3. + ((H10*H11 + H30*H31)*self.L1)/2. - ((H10*H11 + H30*H31)*self.L2)/2. + (2*H20*H21*self.L3)/3. + ((H10**2 - H11**2 - H30**2 + H31**2)*self.L4)/4., \
                        ((2*H10**2 + 2*H11**2 + 2*H20**2 + 6*H21**2 + 2*H30**2 + 2*H31**2)*self.L0)/6. + ((3*H11**2 + 3*H31**2)*self.L1)/6. + ((3*H10**2 + 3*H30**2)*self.L2)/6. + ((-H10**2 - H11**2 + 2*H20**2 + 6*H21**2 - H30**2 - H31**2)*self.L3)/6. + ((3*H10*H11 - 3*H30*H31)*self.L4)/6. - self.M0/np.sqrt(3) + thcorr, \
                        (2*H21*H30*self.L0)/3. + (H20*H31*self.L1)/2. + ((6*H21*H30 - 3*H20*H31)*self.L2)/6. - (H21*H30*self.L3)/3. + ((-3*H20*H30 - 3*H21*H31)*self.L4)/6., \
                        (2*H21*H31*self.L0)/3. + ((3*H20*H30 + 6*H21*H31)*self.L1)/6. - (H20*H30*self.L2)/2. - (H21*H31*self.L3)/3. + ((-3*H21*H30 + 3*H20*H31)*self.L4)/6.], \
                       [(2*H10*H30*self.L0)/3. + ((6*H10*H30 + 3*H11*H31)*self.L1)/6. - (H11*H31*self.L2)/2. - (H10*H30*self.L3)/3. + ((3*H11*H30 - 3*H10*H31)*self.L4)/6., \
                        (2*H11*H30*self.L0)/3. + (H10*H31*self.L1)/2. + ((6*H11*H30 - 3*H10*H31)*self.L2)/6. - (H11*H30*self.L3)/3. + ((3*H10*H30 + 3*H11*H31)*self.L4)/6., \
                        (2*H20*H30*self.L0)/3. + ((6*H20*H30 + 3*H21*H31)*self.L1)/6. - (H21*H31*self.L2)/2. - (H20*H30*self.L3)/3. + ((-3*H21*H30 + 3*H20*H31)*self.L4)/6., \
                        (2*H21*H30*self.L0)/3. + (H20*H31*self.L1)/2. + ((6*H21*H30 - 3*H20*H31)*self.L2)/6. - (H21*H30*self.L3)/3. + ((-3*H20*H30 - 3*H21*H31)*self.L4)/6., \
                        ((2*H10**2 + 2*H11**2 + 2*H20**2 + 2*H21**2 + 6*H30**2 + 2*H31**2)*self.L0)/6. + ((3*H10**2 + 3*H20**2)*self.L1)/6. + ((3*H11**2 + 3*H21**2)*self.L2)/6. + ((-H10**2 - H11**2 - H20**2 - H21**2 + 6*H30**2 + 2*H31**2)*self.L3)/6. + ((3*H10*H11 - 3*H20*H21)*self.L4)/6. - self.M0/np.sqrt(3) + thcorr, \
                        (2*H30*H31*self.L0)/3. + ((H10*H11 + H20*H21)*self.L1)/2. - ((H10*H11 + H20*H21)*self.L2)/2. + (2*H30*H31*self.L3)/3. + ((-H10**2 + H11**2 + H20**2 - H21**2)*self.L4)/4.], \
                       [(2*H10*H31*self.L0)/3. + (H11*H30*self.L1)/2. + ((-3*H11*H30 + 6*H10*H31)*self.L2)/6. - (H10*H31*self.L3)/3. + ((-3*H10*H30 - 3*H11*H31)*self.L4)/6., \
                        (2*H11*H31*self.L0)/3. + ((3*H10*H30 + 6*H11*H31)*self.L1)/6. - (H10*H30*self.L2)/2. - (H11*H31*self.L3)/3. + ((3*H11*H30 - 3*H10*H31)*self.L4)/6., \
                        (2*H20*H31*self.L0)/3. + (H21*H30*self.L1)/2. + ((-3*H21*H30 + 6*H20*H31)*self.L2)/6. - (H20*H31*self.L3)/3. + ((3*H20*H30 + 3*H21*H31)*self.L4)/6., \
                        (2*H21*H31*self.L0)/3. + ((3*H20*H30 + 6*H21*H31)*self.L1)/6. - (H20*H30*self.L2)/2. - (H21*H31*self.L3)/3. + ((-3*H21*H30 + 3*H20*H31)*self.L4)/6., \
                        (2*H30*H31*self.L0)/3. + ((H10*H11 + H20*H21)*self.L1)/2. - ((H10*H11 + H20*H21)*self.L2)/2. + (2*H30*H31*self.L3)/3. + ((-H10**2 + H11**2 + H20**2 - H21**2)*self.L4)/4., \
                        ((2*H10**2 + 2*H11**2 + 2*H20**2 + 2*H21**2 + 2*H30**2 + 6*H31**2)*self.L0)/6. + ((3*H11**2 + 3*H21**2)*self.L1)/6. + ((3*H10**2 + 3*H20**2)*self.L2)/6. + ((-H10**2 - H11**2 - H20**2 - H21**2 + 2*H30**2 + 6*H31**2)*self.L3)/6. + ((-3*H10*H11 + 3*H20*H21)*self.L4)/6. - self.M0/np.sqrt(3) + thcorr]])
        
        # Swapping axes so the last two axes correspond to the matrices. Necessary to compute eigenvalues.
        nm = np.moveaxis(nm, [0, 1], [-2, -1])
        cm = np.moveaxis(cm, [0, 1], [-2, -1])

        # Physical fields correspond to the eigenvalues of the mass matrix + thermal corrections
        neigvals = np.linalg.eigvalsh(nm)
        ceigvals = np.linalg.eigvalsh(cm)

        # Swapping axes so the first axis correspond to fields
        neigvals = np.moveaxis(neigvals, -1, 0)
        ceigvals = np.moveaxis(ceigvals, -1, 0)

        # V: Vector bosons W+, W-, Z, gam (L = 0, T = +/-1) -- only L-polarisations have to be T-corrected!

        # thermally-corrected longitudinal (L) vector bosons
        gl = 2*self.mW/self.vh
        gy = 2*np.sqrt(self.mZ**2 - self.mW**2)/self.vh
        
        mWL   = (((H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)/4.+11./6.*T**2)*gl**2)

        vm11  = mWL
        vm22  = ((H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)/4.+11./6.*T**2)*gy**2
        vm12  = -gl*gy*(H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)/4.

        mZL   = 0.5*(vm11+vm22+np.sqrt(4*vm12**2+vm11**2-2*vm11*vm22+vm22**2))
        mgamL = 0.5*(vm11+vm22-np.sqrt(4*vm12**2+vm11**2-2*vm11*vm22+vm22**2))

        # thermally-uncorrected transverse (T) vector bosons
        mWT   = (H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)/4.*gl**2
        mZT   = (H10**2 + H11**2 + H20**2 + H21**2 + H30**2 + H31**2)/4.*(gl**2+gy**2)
        
        # M: total boson masses
        M = np.array([neigvals[0].astype(float) ,neigvals[1].astype(float) ,neigvals[2].astype(float) ,neigvals[3].astype(float) ,neigvals[4].astype(float) ,neigvals[5].astype(float) ,ceigvals[0].astype(float) ,ceigvals[1].astype(float) ,ceigvals[2].astype(float) ,ceigvals[3].astype(float) ,ceigvals[4].astype(float) ,ceigvals[5].astype(float) ,mWL,mZL,mgamL,mWT,mZT])

        # The number of degrees of freedom for the masses.
        dof = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 4, 2])
       
        # CW constant
        c = np.array([1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,0.5,0.5])
        
        # Swapping axes so the last axis correspond to fields      
        M = np.rollaxis(M, 0, len(M.shape))

        return M, dof, c

    def fermion_massSq(self, X):
        X = np.array(X)
        H10,H20,H21,H30,H31 = X[...,0], X[...,1], X[...,2], X[...,3], X[...,4] # Extracting array containing multiple values for each individual field
        H11 = np.zeros_like(H10)    

        #Lepton Mass Matrix
        lep_mm = np.array([[1/2.*(self.ye**2 + self.ymuon**2 + self.ytau**2)*(H10**2 + H11**2), \
                            1/4.*(2*self.ye**2 + (-1-1j*np.sqrt(3))*self.ymuon**2 + (-1+1j*np.sqrt(3))*self.ytau**2)*(H11 - H10*1j)*(H21 + H20*1j), \
                            1/4.*(2*self.ye**2 + (-1+1j*np.sqrt(3))*self.ymuon**2 + (-1-1j*np.sqrt(3))*self.ytau**2)*(H11 - H10*1j)*(H31 + H30*1j)], \
                           [1/4.*(2*self.ye**2 + (-1+1j*np.sqrt(3))*self.ymuon**2 + (-1-1j*np.sqrt(3))*self.ytau**2)*(H21 - H20*1j)*(H11 + H10*1j), \
                            1/2.*(self.ye**2 + self.ymuon**2 + self.ytau**2)*(H20**2 + H21**2), \
                            1/4.*(2*self.ye**2 + (-1-1j*np.sqrt(3))*self.ymuon**2 + (-1+1j*np.sqrt(3))*self.ytau**2)*(H21 - H20*1j)*(H31 + H30*1j)], \
                           [1/4.*(2*self.ye**2 + (-1-1j*np.sqrt(3))*self.ymuon**2 + (-1+1j*np.sqrt(3))*self.ytau**2)*(H31 - H30*1j)*(H11 + H10*1j), \
                            1/4.*(2*self.ye**2 + (-1+1j*np.sqrt(3))*self.ymuon**2 + (-1-1j*np.sqrt(3))*self.ytau**2)*(H31 - H30*1j)*(H21 + H20*1j), \
                            1/2.*(self.ye**2 + self.ymuon**2 + self.ytau**2)*(H30**2 + H31**2)]])
        
        #Up-quarks Mass Matrix
        up_mm = np.array([[1/2.*(self.yu**2 + self.yc**2 + self.yt**2)*(H10**2 + H11**2), \
                            1/4.*(2*self.yu**2 + (-1-1j*np.sqrt(3))*self.yc**2 + (-1+1j*np.sqrt(3))*self.yt**2)*(H11 + H10*1j)*(H21 - H20*1j), \
                            1/4.*(2*self.yu**2 + (-1+1j*np.sqrt(3))*self.yc**2 + (-1-1j*np.sqrt(3))*self.yt**2)*(H11 + H10*1j)*(H31 - H30*1j)], \
                           [1/4.*(2*self.yu**2 + (-1+1j*np.sqrt(3))*self.yc**2 + (-1-1j*np.sqrt(3))*self.yt**2)*(H21 + H20*1j)*(H11 - H10*1j), \
                            1/2.*(self.yu**2 + self.yc**2 + self.yt**2)*(H20**2 + H21**2), \
                            1/4.*(2*self.yu**2 + (-1-1j*np.sqrt(3))*self.yc**2 + (-1+1j*np.sqrt(3))*self.yt**2)*(H21 + H20*1j)*(H31 - H30*1j)], \
                           [1/4.*(2*self.yu**2 + (-1-1j*np.sqrt(3))*self.yc**2 + (-1+1j*np.sqrt(3))*self.yt**2)*(H31 + H30*1j)*(H11 - H10*1j), \
                            1/4.*(2*self.yu**2 + (-1+1j*np.sqrt(3))*self.yc**2 + (-1-1j*np.sqrt(3))*self.yt**2)*(H31 + H30*1j)*(H21 - H20*1j), \
                            1/2.*(self.yu**2 + self.yc**2 + self.yt**2)*(H30**2 + H31**2)]])
        
        #Down-quarks Mass Matrix
        down_mm = np.array([[1/2.*(self.yd**2 + self.ys**2 + self.yb**2)*(H10**2 + H11**2), \
                            1/4.*(2*self.yd**2 + (-1-1j*np.sqrt(3))*self.ys**2 + (-1+1j*np.sqrt(3))*self.yb**2)*(H11 - H10*1j)*(H21 + H20*1j), \
                            1/4.*(2*self.yd**2 + (-1+1j*np.sqrt(3))*self.ys**2 + (-1-1j*np.sqrt(3))*self.yb**2)*(H11 - H10*1j)*(H31 + H30*1j)], \
                           [1/4.*(2*self.yd**2 + (-1+1j*np.sqrt(3))*self.ys**2 + (-1-1j*np.sqrt(3))*self.yb**2)*(H21 - H20*1j)*(H11 + H10*1j), \
                            1/2.*(self.yd**2 + self.ys**2 + self.yb**2)*(H20**2 + H21**2), \
                            1/4.*(2*self.yd**2 + (-1-1j*np.sqrt(3))*self.ys**2 + (-1+1j*np.sqrt(3))*self.yb**2)*(H21 - H20*1j)*(H31 + H30*1j)], \
                           [1/4.*(2*self.yd**2 + (-1-1j*np.sqrt(3))*self.ys**2 + (-1+1j*np.sqrt(3))*self.yb**2)*(H31 - H30*1j)*(H11 + H10*1j), \
                            1/4.*(2*self.yd**2 + (-1+1j*np.sqrt(3))*self.ys**2 + (-1-1j*np.sqrt(3))*self.yb**2)*(H31 - H30*1j)*(H21 + H20*1j), \
                            1/2.*(self.ys**2 + self.ys**2 + self.yb**2)*(H30**2 + H31**2)]])
        
        # Swapping axes so the last two axes correspond to the matrices. Necessary to compute eigenvalues.
        lep_mm = np.moveaxis(lep_mm, [0, 1], [-2, -1])
        up_mm = np.moveaxis(up_mm, [0, 1], [-2, -1])
        down_mm = np.moveaxis(down_mm, [0, 1], [-2, -1])
      
        # Physical fields correspond to the eigenvalues of the mass matrix + thermal corrections
        lep_mm_eigvals = np.real(np.linalg.eigvalsh(lep_mm))
        up_mm_eigvals = np.real(np.linalg.eigvalsh(up_mm))
        down_mm_eigvals = np.real(np.linalg.eigvalsh(down_mm))

        # Swapping axes so the first axis correspond to fields
        lep_mm_eigvals = np.moveaxis(lep_mm_eigvals, -1, 0)
        up_mm_eigvals = np.moveaxis(up_mm_eigvals, -1, 0)
        down_mm_eigvals = np.moveaxis(down_mm_eigvals, -1, 0)

        melec2 = lep_mm_eigvals[0].astype(float) 
        mmuon2 = lep_mm_eigvals[1].astype(float) 
        mtau2 = lep_mm_eigvals[2].astype(float) 
        
        mup2 = up_mm_eigvals[0].astype(float) 
        mcharm2 = up_mm_eigvals[1].astype(float) 
        mtop2 = up_mm_eigvals[2].astype(float) 
        
        mdown2 = down_mm_eigvals[0].astype(float) 
        mstrange2 = down_mm_eigvals[1].astype(float) 
        mbot2 = down_mm_eigvals[2].astype(float) 
        
        # M: total boson masses
        M = np.array([mtop2,mbot2,mtau2,mcharm2,mstrange2,mmuon2,mup2,mdown2,melec2])

        # Swapping axes so the last axis correspond to fields  
        M = np.rollaxis(M, 0, len(M.shape))

        # The number of degrees of freedom for the masses.
        dof = np.array([12,12,4,12,12,4,12,12,4])

        return M,dof

    def approxZeroTMin(self):
        # Approximate minimum at T=0. Giving tree-level minimum
        return [np.array([self.vh/np.sqrt(3), self.vh/np.sqrt(3), 0, self.vh/np.sqrt(3), 0])]
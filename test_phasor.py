

import unittest
from phasor import Phasor
import numpy as np

class TestPhasorArithmetic(unittest.TestCase):

    def test_equlity(self):
        v1 = Phasor(1,np.pi/2)
        v2 = Phasor(1,5*np.pi/2)
        self.assertEqual(v1,v2)

    def test_unequality(self):
        v1 = Phasor(1,0)
        v2 = Phasor(1,np.pi/2)
        self.assertNotEqual(v1,v2)

    def test_addition_mag(self):
        mag = 10
        val_is = Phasor(mag,0) + Phasor(mag,np.pi/2)
        val_should = np.sqrt(mag**2 + mag**2)
        self.assertAlmostEqual(val_is.mag,val_should,4)

    def test_addition_phase(self):
        mag = 10
        val_is = Phasor(mag,0) + Phasor(mag,np.pi/2)
        val_should = np.arctan2(val_is.imag,val_is.real)
        if val_should < 0:
            val_should += 2*np.pi 
        self.assertEqual(val_is.phase,val_should)

    def test_sub(self):
        v1 = Phasor(10,0)
        v2 = Phasor(10,np.pi)
        result_is = v1 - v2
        result_should = Phasor(20,0)

        self.assertEqual(result_is,result_should)

        
    def test_scaling(self):
        mag = 2
        scaler = 4
        phase = np.pi/4
        v1 = Phasor(mag,phase)
        v2 = scaler * v1
        self.assertEqual(v2,Phasor(mag*scaler,phase))

    def test_scaling_with_phasor(self):
        mag = 2
        phase = np.pi/3
        v1 = Phasor(mag,phase)
        scaler = Phasor(10,0)
        result = scaler * v1 
        self.assertEqual(result,Phasor(10*mag,phase))

    def test_multiplication(self):
        v1 = Phasor(10,np.pi/3)
        v2 = Phasor(10,np.pi/6)
        result = v1 * v2 
        self.assertAlmostEqual(result.mag,100,4)
        self.assertAlmostEqual(result.phase,(np.pi/3 + np.pi/6),4)

    

    




if __name__ == '__main__':
    unittest.main()
from adder.adder import Calculator


class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_calculate_currectly(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def test_division_calculate_currectly(self):
        assert self.calc.division(self, 6, 3) == 2

    def test_multiply_calculate_not_currectly(self):
        assert self.calc.multiply(self, 2, 2) == 4
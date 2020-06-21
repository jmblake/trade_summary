import unittest
from summary import Summary


class FirstTestCase(unittest.TestCase):
    def setUp(self):
        # A simple test case set up on two symbols. The first four elements are
        # valid test data, but trade_data[4] has a numeric symbol. 
        self.test = Summary("", "")
        # Each list within the trade_data list has the form: 
        # [timeStamp, symbol, quantity, price]
        self.test.trade_data = [['1', 'aaa', '1', '0'], ['2', 'aaa', '1', '1'],
                                ['2', 'bbb', '2', '2'], ['5', 'aaa', '1', '3'],
                                ['7', '123', '2', '3'], ['9', '','1','1'], 
                                ['10', 'ddd', 'large', '10'],
                                ['11', 'ddd', '1.2', '2']]
    
    
class SecondTestCase(unittest.TestCase):
    def setUp(self):
        # A test with a very large input set.
        self.test = Summary("","")
        self.test.trade_data = (10^9) * [['1','aaa','1','1']]
    
    
class SymbolTest(FirstTestCase):
    def test_invalid_symbol(self):
        # A KeyError shouldn't occur in operation unless something has
        # gone very wrong (keys are written before being called).
        with self.assertRaises(KeyError):
            self.test.trade_summary['ccc']
    
    def test_numeric_symbol(self):
        # This could occur in the case that symbols are numeric.
        # I assume that numeric symbols are permitted, else a Raise statement
        # should be added to the main code.
        # Note that all data are initially read from csv as strings.
        self.test.update_symbol_details(self.test.trade_data[4])
        self.assertDictEqual(self.test.trade_summary['123'], 
                             {'time_stamp': 7,
                              'max_gap': 0,
                              'volume': 2,
                              'max_price': 3,
                              'total_price': 6})
        
    def test_empty_symbol(self):
        # The program accepts any nonempty string as a key for the trade
        # summary / trade_data dictionary.    
        with self.assertRaises(ValueError):
              self.test.update_symbol_details(self.test.trade_data[5])      
    
class MaxGapTest(FirstTestCase):
    # It can be assumed that the time gap will never be negative, so this
    # cuts down on the necessary tests in this class.
    def test_row_by_row(self):
        # Here, we add the "rows" of the test trade data in one-by-one, and 
        # ensure that the values written to each symbol's "max_gap" entry are
        # as expected.
        self.test.update_symbol_details(self.test.trade_data[0])
        self.assertEqual(self.test.trade_summary['aaa']['max_gap'], 0)
        self.test.update_symbol_details(self.test.trade_data[1])
        self.assertEqual(self.test.trade_summary['aaa']['max_gap'], 1)
        self.test.update_symbol_details(self.test.trade_data[2])
        self.assertEqual(self.test.trade_summary['aaa']['max_gap'], 1)
        self.assertEqual(self.test.trade_summary['bbb']['max_gap'], 0)
        self.test.update_symbol_details(self.test.trade_data[3])
        self.assertEqual(self.test.trade_summary['aaa']['max_gap'], 3)
        self.assertEqual(self.test.trade_summary['bbb']['max_gap'], 0)
        
        
class QuantityTest(FirstTestCase):
    def test_row_by_row(self):
        # Checking that we receive the expected volumes.
        self.test.update_symbol_details(self.test.trade_data[0])
        self.assertEqual(self.test.trade_summary['aaa']['volume'], 1)
        self.test.update_symbol_details(self.test.trade_data[1])
        self.assertEqual(self.test.trade_summary['aaa']['volume'], 2)
        self.test.update_symbol_details(self.test.trade_data[2])
        self.assertEqual(self.test.trade_summary['aaa']['volume'], 2)
        self.assertEqual(self.test.trade_summary['bbb']['volume'], 2)
        self.test.update_symbol_details(self.test.trade_data[3])
        self.assertEqual(self.test.trade_summary['aaa']['volume'], 3)
        self.assertEqual(self.test.trade_summary['bbb']['volume'], 2)
    
    def test_invalid_quantity(self):
        # Ensuring that a ValueError is raised if the input cannot be passed
        # to int.
        with self.assertRaises(ValueError):
            self.test.update_symbol_details(self.test.trade_data[6])
            self.test.update_symbol_details(self.test.trade_data[7])
            
            
class MaxPriceTest(FirstTestCase):
    def test_row_by_row(self):
        # As before, testing that we receive the expected results.
        self.test.update_symbol_details(self.test.trade_data[0])
        self.assertEqual(self.test.trade_summary['aaa']['max_price'], 0)
        self.test.update_symbol_details(self.test.trade_data[1])
        self.assertEqual(self.test.trade_summary['aaa']['max_price'], 1)
        self.test.update_symbol_details(self.test.trade_data[2])
        self.assertEqual(self.test.trade_summary['aaa']['max_price'], 1)
        self.assertEqual(self.test.trade_summary['bbb']['max_price'], 2)
        self.test.update_symbol_details(self.test.trade_data[3])
        self.assertEqual(self.test.trade_summary['aaa']['max_price'], 3)
        self.assertEqual(self.test.trade_summary['bbb']['max_price'], 2)
        

class LargeInputTest(SecondTestCase):
    def test_large_input(self):
        # This verifies that the program can handle input files with in the 
        # order of 1 billion rows. This should be sufficient.
        for elem in self.test.trade_data:
            self.test.update_symbol_details(elem)
        self.assertDictEqual(self.test.trade_summary['aaa'], 
                                 {'time_stamp': 1,
                                  'max_gap': 0,
                                  'volume': 10^9,
                                  'max_price': 1,
                                  'total_price': 10^9})
    
    
if __name__ == '__main__':
    unittest.main()

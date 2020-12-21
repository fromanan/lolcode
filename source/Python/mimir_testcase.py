import unittest
class TestCase(unittest.TestCase):
    def test_1(self):
        # region Test Case Contents

        from Project7.project import generate_LMAOcode_from_LOLcode, generate_ROFLcode_from_LOLcode
        from Project7.interpreter import interpret
        SEED = 0
        STANDARD_INPUT = "abcdef"

        def strip_leading_whitespace(text):
            lines = [line.lstrip() for line in text.splitlines()]
            return '\n'.join(lines)

        def expect_exception(lolcode_str):
            print(f"LOLcode str:\n{lolcode_str}")
            with self.assertRaises(Exception) as e:
                generate_LMAOcode_from_LOLcode(lolcode_str)
            with self.assertRaises(Exception) as e:
                generate_ROFLcode_from_LOLcode(lolcode_str)
            print("Correctly raised exception")

        def check_output(lolcode_str, expected_output):
            print(f"LOLcode str:\n{lolcode_str}")
            lmaocode = generate_LMAOcode_from_LOLcode(lolcode_str)
            print("Generated LMAOcode:")
            print(lmaocode)
            executed_lmao_output = interpret(lmaocode, 'LMAOcode', seed=SEED, standard_input=STANDARD_INPUT)

            self.assertEqual(expected_output, executed_lmao_output)
            roflcode = generate_ROFLcode_from_LOLcode(lolcode_str)
            print("Generated ROFLcode:")
            print(roflcode)
            executed_rofl_output = interpret(roflcode, 'ROFLcode', seed=SEED, standard_input=STANDARD_INPUT)

            self.assertEqual(expected_output, executed_rofl_output)

        lolcode_str = r"""
        HAI 1.450
        VISIBLE WHATEVR
        HOW IZ I fib YR arg ITZ A NUMBR  MKAY
        	O RLY? FURSTBIGGR 2 AN arg
        	YA RLY
        		FOUND YR 1	
        	NO WAI
        		I HAS A sub_a ITZ A NUMBR AN ITZ DIFF OF arg AN 2
        		I HAS A sub_b ITZ A NUMBR AN ITZ DIFF OF arg AN 1

        		I HAS A fib_a ITZ A NUMBR AN ITZ I IZ fib YR sub_a MKAY
        		I HAS A fib_b ITZ A NUMBR AN ITZ I IZ fib YR sub_b MKAY

        		FOUND YR SUM OF fib_a AN fib_b
        	OIC
        IF U SAY SO ITZ A NUMBR 
        VISIBLE I IZ fib YR 1 MKAY
        VISIBLE WHATEVR
        KTHXBYE
        """
        check_output(lolcode_str, '49\n1\n97\n')
        lolcode_str = r"""
        HAI 1.450
        VISIBLE WHATEVR
        HOW IZ I fib YR arg ITZ A NUMBR  MKAY
        	O RLY? FURSTBIGGR 2 AN arg
        	YA RLY
        		FOUND YR 1	
        	NO WAI
        		I HAS A sub_a ITZ A NUMBR AN ITZ DIFF OF arg AN 2
        		I HAS A sub_b ITZ A NUMBR AN ITZ DIFF OF arg AN 1

        		I HAS A fib_a ITZ A NUMBR AN ITZ I IZ fib YR sub_a MKAY
        		I HAS A fib_b ITZ A NUMBR AN ITZ I IZ fib YR sub_b MKAY

        		FOUND YR SUM OF fib_a AN fib_b
        	OIC
        IF U SAY SO ITZ A NUMBR 
        VISIBLE I IZ fib YR 4 MKAY
        VISIBLE WHATEVR
        KTHXBYE
        """
        check_output(lolcode_str, '49\n5\n97\n')
        lolcode_str = r"""
        HAI 1.450
        VISIBLE WHATEVR
        HOW IZ I fib YR arg ITZ A NUMBR  MKAY
        	O RLY? FURSTBIGGR 2 AN arg
        	YA RLY
        		FOUND YR 1	
        	NO WAI
        		I HAS A sub_a ITZ A NUMBR AN ITZ DIFF OF arg AN 2
        		I HAS A sub_b ITZ A NUMBR AN ITZ DIFF OF arg AN 1

        		I HAS A fib_a ITZ A NUMBR AN ITZ I IZ fib YR sub_a MKAY
        		I HAS A fib_b ITZ A NUMBR AN ITZ I IZ fib YR sub_b MKAY

        		FOUND YR SUM OF fib_a AN fib_b
        	OIC
        IF U SAY SO ITZ A NUMBR 
        VISIBLE I IZ fib YR 6 MKAY
        VISIBLE WHATEVR
        KTHXBYE
        """
        check_output(lolcode_str, '49\n13\n97\n')
        lolcode_str = r"""
        HAI 1.450
        VISIBLE WHATEVR
        HOW IZ I fib YR arg ITZ A NUMBR  MKAY
        	O RLY? FURSTBIGGR 2 AN arg
        	YA RLY
        		FOUND YR 1	
        	NO WAI
        		FOUND YR SUM OF I IZ fib YR DIFF OF arg AN 2 MKAY AN I IZ fib YR DIFF OF arg AN 1 MKAY
        	OIC
        IF U SAY SO ITZ A NUMBR 
        VISIBLE I IZ fib YR 8 MKAY
        VISIBLE WHATEVR
        KTHXBYE
        """
        check_output(lolcode_str, '49\n34\n97\n')

        # endregion Test Case Contents
if __name__ == '__main__':
    unittest.main()
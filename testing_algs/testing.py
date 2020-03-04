import unittest


class TestSum(unittest.TestCase):

    def test_bam(self):
        self.assertEqual(bam('x', 'x', 'x'), ('x', 'x'))
        self.assertEqual(bam('x', 'y', 'x'), ('x', 'xy'))
        self.assertEqual(bam('x', 'xy', 'x'), ('x', 'x'))
        self.assertEqual(bam('y', 'x', 'y'), ('y', 'xy'))
        self.assertEqual(bam('y', 'y', 'y'), ('y', 'y'))
        self.assertEqual(bam('y', 'xy', 'y'), ('y', 'y'))
        self.assertEqual(bam('xy', 'x', 'x'), ('x', 'x'))
        self.assertEqual(bam('xy', 'y', 'x'), ('xy', 'xy'))
        self.assertEqual(bam('xy', 'xy', 'x'), ('x', 'x'))
        self.assertEqual(bam('xy', 'x', 'y'), ('xy', 'xy'))
        self.assertEqual(bam('xy', 'y', 'y'), ('y', 'y'))
        self.assertEqual(bam('xy', 'xy', 'y'), ('y', 'y'))

    def test_am(self):
        self.assertEqual(am('x', 'x'), ('x', 'x'))
        self.assertEqual(am('x', 'y'), ('x', 'xy'))
        self.assertEqual(am('x', 'xy'), ('x', 'x'))
        self.assertEqual(am('y', 'x'), ('y', 'xy'))
        self.assertEqual(am('y', 'y'), ('y', 'y'))
        self.assertEqual(am('y', 'xy'), ('y', 'y'))
        self.assertEqual(am('xy', 'x'), ('xy', 'x'))
        self.assertEqual(am('xy', 'y'), ('xy', 'y'))
        self.assertEqual(am('xy', 'xy'), ('xy', 'xy'))

    def test_ac(self):
        self.assertEqual(ac('x', 'x'), ('x', 'x'))
        self.assertEqual(ac('x', 'y'), ('x', 'x'))
        self.assertEqual(ac('y', 'x'), ('y', 'y'))
        self.assertEqual(ac('y', 'y'), ('y', 'y'))

    def test_bot(self):
        self.assertEqual(bam('s', 'x', 'x'), ('s', 'xy'))
        self.assertEqual(bam('s', 'y', 'y'), ('s', 'y'))
        self.assertEqual(bam('s', 'xy', 'xy'), ('s', 'y'))

        self.assertEqual(am('s', 'x'), ('s', 'xy'))
        self.assertEqual(am('s', 'y'), ('s', 'y'))
        self.assertEqual(am('s', 'xy'), ('s', 'y'))

        self.assertEqual(ac('s', 'x'), ('s', 'y'))
        self.assertEqual(ac('s', 'y'), ('s', 'y'))


def am(i: str, r: str):
    """Implements the approximate majority algorithm."""
    init, recip = i, r

    if recip == 's' or recip == init or init == 'xy':
        pass
    elif init == 's':  # S agents will espouse the y belief
        if recip == 'xy':
            recip = 'y'
        elif recip == 'x':
            recip = 'xy'
    else:  # Agents who receive a belief they do not share will be swapped either to xy or to the initiators state.
        if recip == 'xy':
            recip = init
        else:
            recip = 'xy'

    return init, recip


def bam(i: str, r: str, choice: str):
    """Implements the binary agreement model algorithm."""
    init, recip = i, r

    if recip == 's':
        pass  # Stubborn agents won't learn.
    elif recip == init:
        if recip == 'xy':  # If both agents are compound, they'll come to both share a state at random.
            recip = init = choice
    elif init == 's':
        if recip == 'xy':
            recip = 'y'
        elif recip == 'x':
            recip = 'xy'
    elif init == 'xy':  # If the initiator is compound, it will choose to share a state at random.
        if recip == choice:
            init = choice
        else:
            recip = 'xy'
    else:
        if recip == 'xy':
            recip = init
        else:
            recip = 'xy'

    return init, recip


def ac(i: str, r: str):
    """Implements the always-copy algorithm."""
    init, recip = i, r

    if recip == 's' or recip == init:
        pass
    elif init == 's':  # S agents will espouse the y belief
        recip = 'y'
    else:
        recip = init

    return init, recip


if __name__ == "__main__":
    unittest.main()

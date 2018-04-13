# -*- encoding:utf-8 -*-
import unittest
from unittest import TestCase
from game import Game


class ChessGameTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_the_shortest_game(self):
        game1 = Game()
        self.assertEqual(game1.fen_piece_placement, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')

        self.assertEqual(game1.get_valid_destinations_of_piece_at('G2'), ['G3', 'G4'])
        game1.move_piece('G2', 'G4')
        self.assertEqual(game1.fen_piece_placement, 'rnbqkbnr/pppppppp/8/8/6P1/8/PPPPPP1P/RNBQKBNR')

        self.assertEqual(game1.get_valid_destinations_of_piece_at('E7'), ['E5', 'E6'])
        game1.move_piece('E7', 'E5')
        self.assertEqual(game1.fen_piece_placement, 'rnbqkbnr/pppp1ppp/8/4p3/6P1/8/PPPPPP1P/RNBQKBNR')


if '__main__' == __name__:
    unittest.main()

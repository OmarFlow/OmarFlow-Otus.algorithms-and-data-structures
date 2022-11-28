#  https://gekomad.github.io/Cinnamon/BitboardCalculator/
from typing import Tuple, List


class ChessMoves:
    def __init__(self):
        self.bits: List[int] = self.create_bits()

    def get_king_moves(self, position: int) -> Tuple[int, int]:
        """Ходы короля"""
        kp = 1 << position
        no_a = 18374403900871474942
        no_h = 9187201950435737471
        k_a = kp & no_a
        k_h = kp & no_h
        moves = k_a << 7\
            | kp << 8\
            | k_h << 9\
            | k_a >> 1\
            | k_h << 1\
            | k_a >> 9\
            | kp >> 8\
            | k_h >> 7
        moves_count = self.moves_count(moves)
        return moves, moves_count

    def get_horse_moves(self, position: int) -> Tuple[int, int]:
        """Ходы коня"""
        hp = 1 << position
        no_ab = 18229723555195321596
        no_gh = 4557430888798830399
        h_ab = hp & no_ab
        h_gh = hp & no_gh
        moves = h_ab << 6\
            | h_gh << 10\
            | h_ab << 15\
            | h_gh << 17\
            | h_gh >> 6\
            | h_ab >> 10\
            | h_gh >> 15\
            | h_ab >> 17
        moves_count = self.moves_count_cahcing(moves)
        return moves, moves_count

    def get_rook_moves(self, position: int) -> Tuple[int, int]:
        """Ходы ладьи"""
        y = 255 << 8 * (21 // 8)
        x = 72340172838076673 << position % 8
        moves = y ^ x
        moves_count = self.moves_count_cahcing(moves)
        return moves, moves_count

    def create_bits(self) -> List[int]:
        """Создание кэша для подсчета ходов"""
        bits = []
        for i in range(256):
            bits.append(self.moves_count(i))
        return bits

    def moves_count(self, mask: int) -> int:
        """Подсчёт единичных битов(ходов)"""
        cnt = 0
        while mask > 0:
            if mask & 1 == 1:
                cnt += 1
            mask >>= 1
        return cnt

    def moves_count_cahcing(self, mask: int) -> int:
        """Подсчёт единичных битов(ходов) с помощью кэша"""
        cnt = 0
        while mask > 0:
            cnt += self.bits[mask & 255]
            mask >>= 8
        return cnt

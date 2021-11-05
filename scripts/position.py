import re


class Position():
    def __init__(self):

        # 開始局面
        # Example:
        # P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
        # P2 * -HI *  *  *  *  * -KA *
        # P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
        # P4 *  *  *  *  *  *  *  *  *
        # P5 *  *  *  *  *  *  *  *  *
        # P6 *  *  *  *  *  *  *  *  *
        # P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
        # P8 * +KA *  *  *  *  * +HI *
        # P9+KY+KE+GI+KI+OU+KI+GI+KE+KY
        self._patternP = re.compile(
            r"^P(\d)(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})$")

        # 将棋盤
        self._board = [''] * 100

        # 持駒の数 [未使用, ▲飛, ▲角, ▲金, ▲銀, ▲桂, ▲香, ▲歩, ▽飛, ▽角, ▽金, ▽銀, ▽桂, ▽香, ▽歩]
        self._hands = [0] * 15

    def printBoard(self):
        """将棋盤の描画"""

        # 後手の持ち駒
        a = '{: >3}'.format(self._hands[8])
        b = '{: >3}'.format(self._hands[9])
        c = '{: >3}'.format(self._hands[10])
        d = '{: >3}'.format(self._hands[11])
        e = '{: >3}'.format(self._hands[12])
        f = '{: >3}'.format(self._hands[13])
        g = '{: >3}'.format(self._hands[14])
        print(f" HI  KA  KI  GI  KE  KY  FU  ")
        print(f"+---+---+---+---+---+---+---+")
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|")
        print(f"+---+---+---+---+---+---+---+")
        print(f"")
        # 盤
        print(f"  9   8   7   6   5   4   3   2   1    ")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[91])
        b = '{: >3}'.format(self._board[81])
        c = '{: >3}'.format(self._board[71])
        d = '{: >3}'.format(self._board[61])
        e = '{: >3}'.format(self._board[51])
        f = '{: >3}'.format(self._board[41])
        g = '{: >3}'.format(self._board[31])
        h = '{: >3}'.format(self._board[21])
        i = '{: >3}'.format(self._board[11])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 1")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[92])
        b = '{: >3}'.format(self._board[82])
        c = '{: >3}'.format(self._board[72])
        d = '{: >3}'.format(self._board[62])
        e = '{: >3}'.format(self._board[52])
        f = '{: >3}'.format(self._board[42])
        g = '{: >3}'.format(self._board[32])
        h = '{: >3}'.format(self._board[22])
        i = '{: >3}'.format(self._board[12])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 2")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[93])
        b = '{: >3}'.format(self._board[83])
        c = '{: >3}'.format(self._board[73])
        d = '{: >3}'.format(self._board[63])
        e = '{: >3}'.format(self._board[53])
        f = '{: >3}'.format(self._board[43])
        g = '{: >3}'.format(self._board[33])
        h = '{: >3}'.format(self._board[23])
        i = '{: >3}'.format(self._board[13])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 3")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[94])
        b = '{: >3}'.format(self._board[84])
        c = '{: >3}'.format(self._board[74])
        d = '{: >3}'.format(self._board[64])
        e = '{: >3}'.format(self._board[54])
        f = '{: >3}'.format(self._board[44])
        g = '{: >3}'.format(self._board[34])
        h = '{: >3}'.format(self._board[24])
        i = '{: >3}'.format(self._board[14])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 4")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[95])
        b = '{: >3}'.format(self._board[85])
        c = '{: >3}'.format(self._board[75])
        d = '{: >3}'.format(self._board[65])
        e = '{: >3}'.format(self._board[55])
        f = '{: >3}'.format(self._board[45])
        g = '{: >3}'.format(self._board[35])
        h = '{: >3}'.format(self._board[25])
        i = '{: >3}'.format(self._board[15])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 5")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[96])
        b = '{: >3}'.format(self._board[86])
        c = '{: >3}'.format(self._board[76])
        d = '{: >3}'.format(self._board[66])
        e = '{: >3}'.format(self._board[56])
        f = '{: >3}'.format(self._board[46])
        g = '{: >3}'.format(self._board[36])
        h = '{: >3}'.format(self._board[26])
        i = '{: >3}'.format(self._board[16])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 6")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[97])
        b = '{: >3}'.format(self._board[87])
        c = '{: >3}'.format(self._board[77])
        d = '{: >3}'.format(self._board[67])
        e = '{: >3}'.format(self._board[57])
        f = '{: >3}'.format(self._board[47])
        g = '{: >3}'.format(self._board[37])
        h = '{: >3}'.format(self._board[27])
        i = '{: >3}'.format(self._board[17])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 7")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[98])
        b = '{: >3}'.format(self._board[88])
        c = '{: >3}'.format(self._board[78])
        d = '{: >3}'.format(self._board[68])
        e = '{: >3}'.format(self._board[58])
        f = '{: >3}'.format(self._board[48])
        g = '{: >3}'.format(self._board[38])
        h = '{: >3}'.format(self._board[28])
        i = '{: >3}'.format(self._board[18])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 8")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a = '{: >3}'.format(self._board[99])
        b = '{: >3}'.format(self._board[89])
        c = '{: >3}'.format(self._board[79])
        d = '{: >3}'.format(self._board[69])
        e = '{: >3}'.format(self._board[59])
        f = '{: >3}'.format(self._board[49])
        g = '{: >3}'.format(self._board[39])
        h = '{: >3}'.format(self._board[29])
        i = '{: >3}'.format(self._board[19])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 9")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        # 先手の持ち駒
        print(f"")
        a = '{: >3}'.format(self._hands[1])
        b = '{: >3}'.format(self._hands[2])
        c = '{: >3}'.format(self._hands[3])
        d = '{: >3}'.format(self._hands[4])
        e = '{: >3}'.format(self._hands[5])
        f = '{: >3}'.format(self._hands[6])
        g = '{: >3}'.format(self._hands[7])
        print(f"         HI  KA  KI  GI  KE  KY  FU  ")
        print(f"        +---+---+---+---+---+---+---+")
        print(f"        |{a}|{b}|{c}|{d}|{e}|{f}|{g}|")
        print(f"        +---+---+---+---+---+---+---+")


# Test
# python.exe "./scripts/position.py"
if __name__ == "__main__":

    position = Position()
    position.printBoard()

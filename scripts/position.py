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
        self._begin_pos_pattern = re.compile(
            r"^P(\d)(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})$")

        # 指し手
        # Example: +7776FU
        # Example: -8384FU
        self._move_pattern = re.compile(r"^([+-])(\d{2})(\d{2})(\w{2})$")

        # 将棋盤
        self._board = [''] * 100

        # 持駒の数 [未使用, ▲飛, ▲角, ▲金, ▲銀, ▲桂, ▲香, ▲歩, ▽飛, ▽角, ▽金, ▽銀, ▽桂, ▽香, ▽歩]
        self._hands = [0] * 15

    def parse_line(self, line):
        # 開始局面
        matched = self._begin_pos_pattern.match(line)
        if matched:
            rank = int(matched.group(1))
            self._board[90 + rank] = matched.group(2)
            self._board[80 + rank] = matched.group(3)
            self._board[70 + rank] = matched.group(4)
            self._board[60 + rank] = matched.group(5)
            self._board[50 + rank] = matched.group(6)
            self._board[40 + rank] = matched.group(7)
            self._board[30 + rank] = matched.group(8)
            self._board[20 + rank] = matched.group(9)
            self._board[10 + rank] = matched.group(10)

            return

        # 指し手
        result = self._move_pattern.match(line)
        if result:
            phase = result.group(1)
            source = int(result.group(2))
            destination = int(result.group(3))
            piece = result.group(4)
            srcPc = self._board[source]  # sourcePiece
            dstPc = self._board[destination]  # destinationPiece
            # print(f"Move> {result.group(0)} [phase]{phase:>2} [source]{source:>2} [destination]{destination} [piece]{piece} srcPc[{srcPc}] dstPc[{dstPc}]")
            if source != 0 and srcPc == ' * ':
                raise Exception("空マスから駒を動かそうとしました")

            # 駒を打つとき、駒台から減らす
            if source == 0:
                if phase == '+':
                    srcPc = '+{}'.format(piece)
                    if piece == 'FU':
                        self._hands[7] -= 1
                    elif piece == 'KY':
                        self._hands[6] -= 1
                    elif piece == 'KE':
                        self._hands[5] -= 1
                    elif piece == 'GI':
                        self._hands[4] -= 1
                    elif piece == 'KI':
                        self._hands[3] -= 1
                    elif piece == 'KA':
                        self._hands[2] -= 1
                    elif piece == 'HI':
                        self._hands[1] -= 1
                    else:
                        raise Exception(f"+ phase={phase} piece={piece}")
                elif phase == '-':
                    srcPc = '-{}'.format(piece)
                    if piece == 'FU':
                        self._hands[14] -= 1
                    elif piece == 'KY':
                        self._hands[13] -= 1
                    elif piece == 'KE':
                        self._hands[12] -= 1
                    elif piece == 'GI':
                        self._hands[11] -= 1
                    elif piece == 'KI':
                        self._hands[10] -= 1
                    elif piece == 'KA':
                        self._hands[9] -= 1
                    elif piece == 'HI':
                        self._hands[8] -= 1
                    else:
                        raise Exception(f"- phase={phase} piece={piece}")

            # 移動先に駒があれば駒台へ移動
            if phase == '+':
                if dstPc == "-FU" or dstPc == "-TO":
                    self._hands[7] += 1
                elif dstPc == "-KY" or dstPc == "-NY":
                    self._hands[6] += 1
                elif dstPc == "-KE" or dstPc == "-NK":
                    self._hands[5] += 1
                elif dstPc == "-GI" or dstPc == "-NG":
                    self._hands[4] += 1
                elif dstPc == "-KI":
                    self._hands[3] += 1
                elif dstPc == "-KA" or dstPc == "-UM":
                    self._hands[2] += 1
                elif dstPc == "-HI" or dstPc == "-RY":
                    self._hands[1] += 1
                elif dstPc == "-OU":
                    pass
            elif phase == '-':
                if dstPc == "+FU" or dstPc == "+TO":
                    self._hands[14] += 1
                elif dstPc == "+KY" or dstPc == "+NY":
                    self._hands[13] += 1
                elif dstPc == "+KE" or dstPc == "+NK":
                    self._hands[12] += 1
                elif dstPc == "+GI" or dstPc == "+NG":
                    self._hands[11] += 1
                elif dstPc == "+KI":
                    self._hands[10] += 1
                elif dstPc == "+KA" or dstPc == "+UM":
                    self._hands[9] += 1
                elif dstPc == "+HI" or dstPc == "+RY":
                    self._hands[8] += 1
                elif dstPc == "+OU":
                    pass
            else:
                raise Exception(f"Caputure piece. phase={phase}")

            # 移動元の駒を消す
            self._board[source] = " * "

            # 移動先に駒を置く
            self._board[destination] = srcPc

            return

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

    position.parse_line('P1-KY-KE-GI-KI-OU-KI-GI-KE-KY')
    position.printBoard()

    position.parse_line('P2 * -HI *  *  *  *  * -KA * ')
    position.printBoard()

    position.parse_line('P3-FU-FU-FU-FU-FU-FU-FU-FU-FU')
    position.printBoard()

    position.parse_line('P4 *  *  *  *  *  *  *  *  * ')
    position.printBoard()

    position.parse_line('P5 *  *  *  *  *  *  *  *  * ')
    position.printBoard()

    position.parse_line('P6 *  *  *  *  *  *  *  *  * ')
    position.printBoard()

    position.parse_line('P7+FU+FU+FU+FU+FU+FU+FU+FU+FU')
    position.printBoard()

    position.parse_line('P8 * +KA *  *  *  *  * +HI * ')
    position.printBoard()

    position.parse_line('P9+KY+KE+GI+KI+OU+KI+GI+KE+KY')
    position.printBoard()

    # 指し手
    # Example: +7776FU
    # Example: -8384FU

    position.parse_line('+7776FU')
    position.printBoard()

    position.parse_line('-8384FU')
    position.printBoard()

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
        self._begin_pos_row_pattern = re.compile(
            r"^P(\d)(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})(.{3})$")

        # 自分または相手の指し手と、その消費時間
        # Format: `<先後><元升><先升><駒>,T<秒>`
        # Example: `+5756FU,T20`
        self._move_pattern = re.compile(
            r"^([+-])(\d{2})(\d{2})(\w{2}),T(\d+)$")

        # 将棋盤
        self._board = [''] * 100

        # 持駒の数 [未使用, ▲飛, ▲角, ▲金, ▲銀, ▲桂, ▲香, ▲歩, ▽飛, ▽角, ▽金, ▽銀, ▽桂, ▽香, ▽歩]
        self._hands = [0] * 15

        # 経過時間 [未使用, 先手, 後手]
        self._expendTimes = [0, 0, 0]

    @property
    def board(self):
        return self._board

    @property
    def hands(self):
        return self._hands

    def parse_line(self, line):
        # 開始局面
        matched = self._begin_pos_row_pattern.match(line)
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

            return '<Position.BeginPosRow/>'

        # 指し手
        result = self._move_pattern.match(line)
        if result:
            phase = result.group(1)
            source = int(result.group(2))
            destination = int(result.group(3))
            expendTime = int(result.group(5))

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

            # 経過時間
            if phase == '+':
                self._expendTimes[1] += expendTime
            else:
                self._expendTimes[2] += expendTime

            return '<Position.Move/>'

        return '<Position.Unknown/>'

    def printBoard(self):
        """将棋盤の描画"""

        def __prettyHands(indexes):
            def __eraseZero(n):
                if n == 0:
                    return ''
                return n

            a = '{: >3}'.format(__eraseZero(self._hands[indexes[0]]))
            b = '{: >3}'.format(__eraseZero(self._hands[indexes[1]]))
            c = '{: >3}'.format(__eraseZero(self._hands[indexes[2]]))
            d = '{: >3}'.format(__eraseZero(self._hands[indexes[3]]))
            e = '{: >3}'.format(__eraseZero(self._hands[indexes[4]]))
            f = '{: >3}'.format(__eraseZero(self._hands[indexes[5]]))
            g = '{: >3}'.format(__eraseZero(self._hands[indexes[6]]))
            return a, b, c, d, e, f, g

        def __prettyBoardRow(indexes):
            def __eraseAsterisk(s):
                if s == ' * ':
                    return '   '
                return s

            a = '{: >3}'.format(__eraseAsterisk(self._board[indexes[0]]))
            b = '{: >3}'.format(__eraseAsterisk(self._board[indexes[1]]))
            c = '{: >3}'.format(__eraseAsterisk(self._board[indexes[2]]))
            d = '{: >3}'.format(__eraseAsterisk(self._board[indexes[3]]))
            e = '{: >3}'.format(__eraseAsterisk(self._board[indexes[4]]))
            f = '{: >3}'.format(__eraseAsterisk(self._board[indexes[5]]))
            g = '{: >3}'.format(__eraseAsterisk(self._board[indexes[6]]))
            h = '{: >3}'.format(__eraseAsterisk(self._board[indexes[7]]))
            i = '{: >3}'.format(__eraseAsterisk(self._board[indexes[8]]))
            return a, b, c, d, e, f, g, h, i

        # 後手の持ち駒、経過時間
        tim2 = f'{self._expendTimes[2]: >6}'
        a, b, c, d, e, f, g = __prettyHands([8, 9, 10, 11, 12, 13, 14])
        print(f"  HI  KA  KI  GI  KE  KY  FU    TIME")
        print(f"|{a} {b} {c} {d} {e} {f} {g}| {tim2}")
        print(f"")
        # 盤
        print(f"  9   8   7   6   5   4   3   2   1    ")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [91, 81, 71, 61, 51, 41, 31, 21, 11])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 1")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [92, 82, 72, 62, 52, 42, 32, 22, 12])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 2")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [93, 83, 73, 63, 53, 43, 33, 23, 13])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 3")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [94, 84, 74, 64, 54, 44, 34, 24, 14])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 4")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [95, 85, 75, 65, 55, 45, 35, 25, 15])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 5")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [96, 86, 76, 66, 56, 46, 36, 26, 16])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 6")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [97, 87, 77, 67, 57, 47, 37, 27, 17])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 7")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [98, 88, 78, 68, 58, 48, 38, 28, 18])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 8")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        a, b, c, d, e, f, g, h, i = __prettyBoardRow(
            [99, 89, 79, 69, 59, 49, 39, 29, 19])
        print(f"|{a}|{b}|{c}|{d}|{e}|{f}|{g}|{h}|{i}| 9")
        print(f"+---+---+---+---+---+---+---+---+---+  ")
        # 先手の経過時間、持ち駒
        tim1 = f'{self._expendTimes[1]: >6}'
        a, b, c, d, e, f, g = __prettyHands([1, 2, 3, 4, 5, 6, 7])
        print(f"")
        print(f"   Time   HI  KA  KI  GI  KE  KY  FU  ")
        print(f" {tim1} |{a} {b} {c} {d} {e} {f} {g}|")
        print(f"")
        print(f". . . . . . . . . . . . . . . . . . . .")
        print(f"")


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
    # Example: +7776FU,T20
    # Example: -8384FU,T1

    position.parse_line('+7776FU,T20')
    position.printBoard()

    position.parse_line('-8384FU,T1')
    position.printBoard()

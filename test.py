from scripts.client_p import ClientP, SplitTextBlock

# Test
# python.exe "./scripts/client_p.py"
if __name__ == "__main__":
    """テストします"""
    client_p = ClientP()

    # Send `LOGIN e-gov-vote-kifuwarabe floodgate-300-10F,egov-kif`
    received = 'LOGIN:egov-kifuwarabe OK'
    client_p.parse_line(received)
    if client_p.state.name == '<LoggedInState/>':
        print('.')
    else:
        print('f')

    received = """BEGIN Game_Summary
Protocol_Version:1.2
Protocol_Mode:Server
Format:Shogi 1.0
Declaration:Jishogi 1.1
Game_ID:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005
Name+:e-gov-vote-kifuwarabe
Name-:Kristallweizen-Core2Duo-P7450
Your_Turn:+
Rematch_On_Draw:NO
To_Move:+
Max_Moves:256
BEGIN Time
Time_Unit:1sec
Total_Time:300
Byoyomi:0
Increment:10
Least_Time_Per_Move:0
END Time
BEGIN Position
P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
P2 * -HI *  *  *  *  * -KA * 
P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
P4 *  *  *  *  *  *  *  *  * 
P5 *  *  *  *  *  *  *  *  * 
P6 *  *  *  *  *  *  *  *  * 
P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
P8 * +KA *  *  *  *  * +HI * 
P9+KY+KE+GI+KI+OU+KI+GI+KE+KY
+
END Position
END Game_Summary
"""

    lines = SplitTextBlock(received)

    for line in lines:
        result = client_p.parse_line(line)

    if client_p.state.name == '<GameState/>':
        print('.')
    else:
        print('f')

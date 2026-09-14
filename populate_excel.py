import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

def populate():
    wb = openpyxl.load_workbook('Facility location techniques - input data.xlsx')

    # 1. Location factor rating
    ws_lfr = wb['Location factor rating']
    ws_lfr['C9'] = '=SUMPRODUCT($B$3:$B$8, C3:C8)'
    ws_lfr['D9'] = '=SUMPRODUCT($B$3:$B$8, D3:D8)'
    ws_lfr['E9'] = '=SUMPRODUCT($B$3:$B$8, E3:E8)'
    ws_lfr['F9'] = '=SUMPRODUCT($B$3:$B$8, F3:F8)'

    # 2. CoG technique
    ws_cog = wb['CoG technique']
    ws_cog['E2'] = '=D2*B2'
    ws_cog['F2'] = '=D2*C2'
    ws_cog['E3'] = '=D3*B3'
    ws_cog['F3'] = '=D3*C3'
    ws_cog['E4'] = '=D4*B4'
    ws_cog['F4'] = '=D4*C4'
    ws_cog['E5'] = '=D5*B5'
    ws_cog['F5'] = '=D5*C5'
    ws_cog['E6'] = '=D6*B6'
    ws_cog['F6'] = '=D6*C6'

    ws_cog['D8'] = '=SUM(D2:D6)'
    ws_cog['D9'] = '=SUM(E2:E6)'
    ws_cog['D10'] = '=SUM(F2:F6)'
    ws_cog['D13'] = '=D9/D8'
    ws_cog['D14'] = '=D10/D8'

    # 3. Load-distance technique
    ws_ld = wb['Load-distance technique']
    # Step 1: Euclidean distances
    for r_idx, c_row in enumerate([11, 12, 13]):
        for c_idx, d_row in enumerate([3, 4, 5, 6, 7]):
            col_letter = openpyxl.utils.get_column_letter(6 + c_idx)
            ws_ld[f'{col_letter}{c_row}'] = f'=SQRT(($B{c_row}-$B${d_row})^2+($C{c_row}-$C${d_row})^2)'

    # Step 2: LD score
    ws_ld['G18'] = '=SUMPRODUCT($D$3:$D$7, F11:J11)'
    ws_ld['G19'] = '=SUMPRODUCT($D$3:$D$7, F12:J12)'
    ws_ld['G20'] = '=SUMPRODUCT($D$3:$D$7, F13:J13)'

    # 4. TM
    ws_tm = wb['TM']
    # Decision variables (optimal flows for Dallas open)
    ws_tm['C12'] = 20000; ws_tm['D12'] = 0;     ws_tm['E12'] = 0;     ws_tm['F12'] = 0;     ws_tm['G12'] = '=SUM(C12:F12)'
    ws_tm['C13'] = 0;     ws_tm['D13'] = 16200; ws_tm['E13'] = 0;     ws_tm['F13'] = 23800; ws_tm['G13'] = '=SUM(C13:F13)'
    ws_tm['C14'] = 9840;  ws_tm['D14'] = 0;     ws_tm['E14'] = 20160; ws_tm['F14'] = 0;     ws_tm['G14'] = '=SUM(C14:F14)'
    ws_tm['C15'] = 160;   ws_tm['D15'] = 0;     ws_tm['E15'] = 0;     ws_tm['F15'] = 17840; ws_tm['G15'] = '=SUM(C15:F15)'
    ws_tm['C16'] = 0;     ws_tm['D16'] = 0;     ws_tm['E16'] = 0;     ws_tm['F16'] = 0;     ws_tm['G16'] = '=SUM(C16:F16)'

    ws_tm['C17'] = '=SUM(C12:C16)'
    ws_tm['D17'] = '=SUM(D12:D16)'
    ws_tm['E17'] = '=SUM(E12:E16)'
    ws_tm['F17'] = '=SUM(F12:F16)'

    ws_tm['B21'] = '=SUMPRODUCT(B2:E6, C12:F16)'
    ws_tm['G23'] = 1
    ws_tm['G24'] = 0
    ws_tm['G25'] = '=SUM(G23:G24)'

    # 5. SCND
    ws_scnd = wb['SCND']
    # Plant binaries & RHS
    ws_scnd['B17'] = 1; ws_scnd['C17'] = '=B17*H12'
    ws_scnd['B18'] = 1; ws_scnd['C18'] = '=B18*H13'
    ws_scnd['B19'] = 0; ws_scnd['C19'] = '=B19*H14'

    # DC binaries & RHS
    ws_scnd['B22'] = 1; ws_scnd['C22'] = '=B22*H19'
    ws_scnd['B23'] = 0; ws_scnd['C23'] = '=B23*H20'
    ws_scnd['B24'] = 0; ws_scnd['C24'] = '=B24*H21'
    ws_scnd['B25'] = 1; ws_scnd['C25'] = '=B25*H22'
    ws_scnd['B26'] = 1; ws_scnd['C26'] = '=B26*H23'

    # Supplier to Plant flow
    ws_scnd['B30'] = 40000; ws_scnd['C30'] = 0;     ws_scnd['D30'] = 0; ws_scnd['E30'] = '=SUM(B30:D30)'
    ws_scnd['B31'] = 0;     ws_scnd['C31'] = 0;     ws_scnd['D31'] = 0; ws_scnd['E31'] = '=SUM(B31:D31)'
    ws_scnd['B32'] = 0;     ws_scnd['C32'] = 32000; ws_scnd['D32'] = 0; ws_scnd['E32'] = '=SUM(B32:D32)'
    ws_scnd['B33'] = '=SUM(B30:B32)'
    ws_scnd['C33'] = '=SUM(C30:C32)'
    ws_scnd['D33'] = '=SUM(D30:D32)'

    # Plant to DC flow
    ws_scnd['B36'] = 30000; ws_scnd['C36'] = 0; ws_scnd['D36'] = 0; ws_scnd['E36'] = 0;     ws_scnd['F36'] = 10000; ws_scnd['G36'] = '=SUM(B36:F36)'
    ws_scnd['B37'] = 0;     ws_scnd['C37'] = 0; ws_scnd['D37'] = 0; ws_scnd['E37'] = 25000; ws_scnd['F37'] = 7000;  ws_scnd['G37'] = '=SUM(B37:F37)'
    ws_scnd['B38'] = 0;     ws_scnd['C38'] = 0; ws_scnd['D38'] = 0; ws_scnd['E38'] = 0;     ws_scnd['F38'] = 0;     ws_scnd['G38'] = '=SUM(B38:F38)'
    ws_scnd['B39'] = '=SUM(B36:B38)'
    ws_scnd['C39'] = '=SUM(C36:C38)'
    ws_scnd['D39'] = '=SUM(D36:D38)'
    ws_scnd['E39'] = '=SUM(E36:E38)'
    ws_scnd['F39'] = '=SUM(F36:F38)'

    # DC to CZ flow
    ws_scnd['B42'] = 6000; ws_scnd['C42'] = 18000; ws_scnd['D42'] = 0;     ws_scnd['E42'] = 0;     ws_scnd['F42'] = 6000; ws_scnd['G42'] = 0;    ws_scnd['H42'] = '=SUM(B42:G42)'
    ws_scnd['B43'] = 0;    ws_scnd['C43'] = 0;     ws_scnd['D43'] = 0;     ws_scnd['E43'] = 0;     ws_scnd['F43'] = 0;    ws_scnd['G43'] = 0;    ws_scnd['H43'] = '=SUM(B43:G43)'
    ws_scnd['B44'] = 0;    ws_scnd['C44'] = 0;     ws_scnd['D44'] = 0;     ws_scnd['E44'] = 0;     ws_scnd['F44'] = 0;    ws_scnd['G44'] = 0;    ws_scnd['H44'] = '=SUM(B44:G44)'
    ws_scnd['B45'] = 0;    ws_scnd['C45'] = 0;     ws_scnd['D45'] = 12000; ws_scnd['E45'] = 10000; ws_scnd['F45'] = 3000; ws_scnd['G45'] = 0;    ws_scnd['H45'] = '=SUM(B45:G45)'
    ws_scnd['B46'] = 9000; ws_scnd['C46'] = 0;     ws_scnd['D46'] = 0;     ws_scnd['E46'] = 0;     ws_scnd['F46'] = 0;    ws_scnd['G46'] = 8000; ws_scnd['H46'] = '=SUM(B46:G46)'

    ws_scnd['B47'] = '=SUM(B42:B46)'
    ws_scnd['C47'] = '=SUM(C42:C46)'
    ws_scnd['D47'] = '=SUM(D42:D46)'
    ws_scnd['E47'] = '=SUM(E42:E46)'
    ws_scnd['F47'] = '=SUM(F42:F46)'
    ws_scnd['G47'] = '=SUM(G42:G46)'

    # Echelon totals
    ws_scnd['D49'] = '=SUM(H42:H46)'
    ws_scnd['D50'] = '=SUM(G36:G38)'
    ws_scnd['D51'] = '=SUM(E30:E32)'

    # Objective function components in Col J
    ws_scnd['J30'] = '=SUMPRODUCT(K5:M7, B30:D32)'
    ws_scnd['J31'] = '=SUMPRODUCT(K12:O14, B36:F38)'
    ws_scnd['J32'] = '=SUMPRODUCT(K19:P23, B42:G46)'
    ws_scnd['J33'] = '=SUMPRODUCT(G12:G14, B17:B19)'
    ws_scnd['J34'] = '=SUMPRODUCT(G19:G23, B22:B26)'
    ws_scnd['J35'] = '=SUM(J30:J34)'

    wb.save('Facility location techniques - input data.xlsx')
    print('Successfully populated and saved Facility location techniques - input data.xlsx')

if __name__ == '__main__':
    populate()

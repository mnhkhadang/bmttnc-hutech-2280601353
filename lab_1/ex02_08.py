def chia_het_cho_5 (so_nhi_phan):
    #chuyen nhi phan sang thap phan 
    so_thap_phan = int(so_nhi_phan, 2)
    #kiem tra so thap phan chia het cho 5 hong
    if so_thap_phan % 5 == 0:
        return True
    else:
        return False
    
chuoi_nhi_phan = input("nhap chuoi so nhi phan ")

so_nhi_phan_list = chuoi_nhi_phan.split(',')
chia_het_cho_5 = [so for so in so_nhi_phan_list if chia_het_cho_5(so)]
if len(chia_het_cho_5) > 0:
    ketqua =','.join(chia_het_cho_5)
else:
    print("ko co so nhi phan nao chia het cho 5 torng chuoi da nhap") 
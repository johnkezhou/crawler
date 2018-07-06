# --*-- coding:utf-8 --*--


class cookies(object):
    info = []
    
    def __init__(self):
        tmp2 ={}
        tmp2['cookie'] = {"Cookie": "_T_WM=f161db2617158095e3c1aff96bed9c21; gsid_CTandWM=4uLVCpOz5nNgHpCnH2w1oolHybx; SUB=_2A2574I9ODeTxGeNG61ET-SjLyjmIHXVZKhEGrDV6PUJbrdAKLVXZkW1LHesacfEP_sF9RdF2spsMPCY0uZnHcg..; SUHB=0ft5uRNTKQ6Y6Z; SSOLoginState=1457848094; M_WEIBOCN_PARAMS=uicode%3D20000174"}
        tmp2['header'] = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'} ;

        tmp1 ={}
        tmp1['cookie'] = {"Cookie": "_T_WM=f161db2617158095e3c1aff96bed9c21; _WEIBO_UID=5882087268; _T_H5TOWAP=1; backURL=http%3A%2F%2Fm.weibo.cn%2F; curl=http%3A%2F%2Fm.weibo.cn%2F%3Ffrom%3Dh5%26wm%3D3349; H5_wentry=H5; WEIBOCN_WM=3349; H5_INDEX=3; H5_INDEX_TITLE=%E5%86%8D%E8%AF%95%E4%B8%80%E6%AC%A1%E8%BD%B6%E4%BA%8B; SUB=_2A257_guoDeTRGeNG41sY9S3OyT-IHXVZAJXgrDV6PUJbrdAKLUetkW1LHetgeLUr_jsdtBD301VeHwSzLkq8MA..; SUHB=0oU4YG7jEQTKiw; SSOLoginState=1459256312; M_WEIBOCN_PARAMS=uicode%3D20000174; gsid_CTandWM=4ujiCpOz5Eu2QQOLrRAsRoIff3B"}
        tmp1['header'] =  {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'} ;

        tmp3 ={}
        tmp3['cookie'] = {"Cookie": "_T_WM=f161db2617158095e3c1aff96bed9c21; _WEIBO_UID=5882087268; backURL=http%3A%2F%2Fm.weibo.cn%2F; H5_wentry=H5; SUHB=0BL4HtUXvMJsnD; H5_INDEX=3; H5_INDEX_TITLE=%E7%A8%8B%E5%BA%8F%E5%91%98%E9%9D%A2%E9%9C%B8; M_WEIBOCN_PARAMS=uicode%3D20000173"}
        tmp3['header'] =  {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'} ;

        self.info.append(tmp1)
        self.info.append(tmp2)
        self.info.append(tmp3)
    def printinfo(self):
        for each in self.info:
            for key in each:
                print key, " : ", each[key]
        return
    
if __name__ == '__main__':
    a = cookies()
    a.printinfo()
        
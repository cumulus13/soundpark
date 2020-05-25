def makeList(alist, ncols, vertically=True, file=None):
        '''
            **Print list with indent input**
            
            ``params:``
                * `alist: list object => list`
                * `ncols: indent or numers of colums => int`
                * `vertically: print list to vertical (left to right), default horizontal (top to buttom) => bool`
            
            ``return:``
                `None`
                
            ``example:``
                >>> s = subscene()
                >>> ['01. data01', '02. data02', '03. data03', '04. data04', '05. data05', '06. data06', '07. data07', '08. data08', '09. data09', '10. data10']
                >>> s.makeList(data, 2)
                >>> 01. data01   06. data06
                    02. data02   07. data07
                    03. data03   08. data08
                    04. data04   09. data09
                    05. data05   10. data10
        '''
        from distutils.version import StrictVersion # pep 386
        import prettytable as ptt # pip install prettytable
        import sys
        assert StrictVersion(ptt.__version__) >= StrictVersion('0.7') # for PrettyTable.vrules property        
        L = alist
        nrows = - ((-len(L)) // ncols)
        ncols = - ((-len(L)) // nrows)
        t = ptt.PrettyTable([str(x) for x in range(ncols)])
        t.header = False
        t.align = 'l'
        t.hrules = ptt.NONE
        t.vrules = ptt.NONE
        r = nrows if vertically else ncols
        chunks = [L[i:i+r] for i in range(0, len(L), r)]
        chunks[-1].extend('' for i in range(r - len(chunks[-1])))
        if vertically:
            chunks = zip(*chunks)
        for c in chunks:
            t.add_row(c)
        print(t)

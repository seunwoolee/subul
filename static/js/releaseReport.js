class Main {
    constructor(rows, address_category, title) {
        this.setLocationCategory(address_category);
        this.setTitle(title);
        this.setLocationCatRowspan(rows.length + 1);
        this.rowsLenth = rows.length;

        try {
            this.diffLocation = rows[0].locationCodeName;
            this.diffPallet = rows[0].pallet_seq;
        } catch (e) {
            alert('데이터를 확인해주세요(지역 카테고리가 다릅니다)');
            return
        }

        this.locationCodeNames = [0];
        this.pallet_seqs = [0];
        this.lastIndex = 0;

        for (let [i, row] of rows.entries()) {
            if (this.diffLocation !== row.locationCodeName) {
                this.locationCodeNames.push(i);
                this.diffLocation = row.locationCodeName;
            }

            if (this.diffPallet !== row.pallet_seq) {
                this.pallet_seqs.push(i);
                this.diffPallet = row.pallet_seq;
            }

            this.insertTr(row, i);
            this.lastIndex = i + 1;
        }

        // 거래처명 rowSpan
        for (let [index, elementSeq] of this.locationCodeNames.entries()) {
            let nextElementSeq = this.locationCodeNames[index + 1];
            if (!nextElementSeq) {
                nextElementSeq = this.lastIndex;
            }

            let offsets = nextElementSeq - elementSeq;
            $('.locationCodeName' + elementSeq).attr('rowspan', offsets);

            for (let j = elementSeq + 1; j < elementSeq + offsets; j++) {
                $('.locationCodeName' + j).remove();
            }
        }

        // 팔레트 NO, 서명 rowSpan
        for (let [index, elementSeq] of this.pallet_seqs.entries()) {
            let nextElementSeq = this.pallet_seqs[index + 1];
            if (!nextElementSeq) {
                nextElementSeq = this.lastIndex;
            }
            let offsets = nextElementSeq - elementSeq;
            let height = offsets * 19;
            $('.pallet_seq' + elementSeq).attr('rowspan', offsets);
            $('.pallet_seq' + elementSeq + ' table').css('height', height);

            for (let j = elementSeq + 1; j < elementSeq + offsets; j++) {
                $('.pallet_seq' + j).remove();
            }
        }
        this.setDetailReport(rows);
    }

    insertTr(row, i) {
        const className = this.getClassName(row.product_type);

        const tr = `<tr>
            <td class="locationCodeName${i}">${row.locationCodeName}</td>
            <td class="pallet_seq${i}">${row.pallet_seq}</td>
            <td class="${className}">${row.codeName}</td>
            <td class="${className}">${row.count}</td>
            <td class="${className}">${row.box}</td>
            <td class="${className}">${row.ea}</td>
            <td class="pallet_seq${i}">
                <div>
                <table>
                    <tr>
                        <td class="bottomBorderRightOnly">&nbsp&nbsp&nbsp&nbsp</td>
                        <td class="borderZero" >&nbsp&nbsp&nbsp&nbsp</td>
                    </tr>
                </table>                 
                </div>
           
            </td>
        </tr>`;
        $('.table').append(tr);
    }

    getClassName(type) {
        if (type === '전란') {
            return "junran"
        } else if (type === '난백') {
            return "nanbak"
        } else if (type === '난황') {
            return "nanhwang"
        }
        return "etc"
    }

    setTitle(title) {
        $('.titleDiv').text(title)
    }

    setLocationCatRowspan(length) {
        $('.locationCategory').attr('rowspan', length);
    }

    setLocationCategory(address_category) {
        let text = '';
        for (let word of address_category) {
            text += word;
            text += '<br>';
        }
        $('.locationCategory').append(text)
    }

    setDetailReport(rows) {
        rows.length !== 1 ? this.pallet_seqs.push(rows.length-1): this.pallet_seqs.push(rows.length);
        rows.forEach((row, index) => {
            if(this.pallet_seqs.length > 1){
                console.log(this.pallet_seqs);
                let detailPage = `
                <page style="font-size: 1.5rem; " size="A4" layout="landscape">
                    <table>
                        <tr>
                            <th>팔레트NO</th>
                            <th>거래처명</th>
                            <th>품목명</th>
                            <th>수량</th>
                            <th>Box</th>
                            <th>EA</th>
                        </tr>
                        ${rows.filter(this.palletSeqBetween.bind(this)).map(row => this.setDetailContent(row)).join('')}

                    </table>
                </page>`;
                $('body').append(detailPage);
                this.pallet_seqs.shift();
            }
        })
    }

    setDetailContent(row) {
        return `
                <tr>
                    <td>${row.pallet_seq}</td>
                    <td>${row.locationCodeName}</td>
                    <td>${row.codeName}</td>
                    <td>${row.count}</td>
                    <td>${row.box}</td>
                    <td>${row.ea}</td>
                </tr>`
    }

    palletSeqBetween(value, index) {
        const start = this.pallet_seqs[0];
        const end = this.pallet_seqs[1];
        if(!this.pallet_seqs[2]){
            // contain last tr content
            return start <= index && index <= end
        }
        return start <= index && index < end
    }

}

main = new Main(rows, address_category, title);

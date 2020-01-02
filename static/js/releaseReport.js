class Main {
    constructor(rows, address_category, title) {
        this.setLocationCategory(address_category);
        this.setTitle(title);

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

        for (let [i, row] of rows.entries()){
            if(this.diffLocation !== row.locationCodeName){
                this.locationCodeNames.push(i);
                this.diffLocation = row.locationCodeName;
            }

            if(this.diffPallet !== row.pallet_seq){
                this.pallet_seqs.push(i);
                this.diffPallet = row.pallet_seq;
            }

            this.insertTr(row, i);
            this.lastIndex = i + 1;
        }

        // 거래처명 rowSpan
        for(let [index, elementSeq] of this.locationCodeNames.entries()){
            let nextElementSeq = this.locationCodeNames[index+1];
            if(!nextElementSeq){
                nextElementSeq = this.lastIndex;
            }

            let offsets = nextElementSeq - elementSeq;
            $('.locationCodeName'+elementSeq).attr('rowspan', offsets);

            for(let j=elementSeq+1; j<elementSeq+offsets; j++ ){
                $('.locationCodeName'+j).remove();
            }
        }

        // 팔레트 NO rowSpan
        for(let [index, elementSeq] of this.pallet_seqs.entries()){
            let nextElementSeq = this.pallet_seqs[index+1];
            if(!nextElementSeq){
                nextElementSeq = this.lastIndex;
            }
            let offsets = nextElementSeq - elementSeq;
            $('.pallet_seq'+elementSeq).attr('rowspan', offsets);

            for(let j=elementSeq+1; j<elementSeq+offsets; j++ ){
                $('.pallet_seq'+j).remove();
            }
        }
    }

    insertTr(row, i) {
        const tr =  `<tr>
            <td class="locationCodeName${i}">${row.locationCodeName}</td>
            <td class="pallet_seq${i}">${row.pallet_seq}</td>
            <td>${row.codeName}</td>
            <td>${row.count}</td>
            <td>${row.box}</td>
            <td>${row.ea}</td>
            <td>
                <table>
                    <tr>
                        <td class="bottomBorderRightOnly">&nbsp&nbsp&nbsp&nbsp</td>
                        <td class="borderZero" >&nbsp&nbsp&nbsp&nbsp</td>
                    </tr>
                </table>
            </td>
        </tr>`;
        $('.table').append(tr);
    }

    setTitle(title){
        $('.titleDiv').text(title)
    }

    setLocationCategory(address_category){
        let text = '';
        for(let word of address_category){
            text += word;
            text += '<br>';
        }
        $('.locationCategory').append(text)
    }

}

main = new Main(rows, address_category, title);

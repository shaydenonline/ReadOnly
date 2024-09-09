//method for making post request that send data to the python
document.addEventListener('click', clickFunction);
function clickFunction(event){
    const translateGrid=document.querySelector('.superContainer');
    if(!translateGrid.contains(event.target)){
        translateGrid.textContent="";
    }
}
const popUpContainer=document.getElementById('popUpContainer');
console.log(`popUpContainer display ${popUpContainer.display}, popUpContainer children`, popUpContainer.childNodes);
document.addEventListener("DOMContentLoaded", function(){
    const hindiParagraph=document.getElementById("hindiText");
    const translate_url=hindiParagraph.getAttribute("href");
    window.addEventListener("mouseup", function(event){
        const hindiSelection=window.getSelection().toString().trim();;
        let phraseRegex=/\S\s\S/;
        let wordRegex=/\p{Script=Devanagari}+/u;

        //check if the highlighted selection is a phrase instead of a word 
        const hiddenWordButtons = document.getElementById("hiddenWordButtons");
        const hiddenPhraseButtons= document.getElementById("hiddenPhraseButtons");
        if(hindiSelection.match(phraseRegex)){
            
            function translatePhraseFunction(){
                attemptedTranslation=window.prompt("Attempt to translate the phrase and see if you went wrong");
                const request=new Request(translate_url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ selection: hindiSelection, attemptedTranslation: attemptedTranslation, type: "phrase" })
                });
                fetch(request);
            }
            document.getElementById('translatePhraseButton').onclick=translatePhraseFunction;
            hiddenPhraseButtons.style.display="block";
            hiddenWordButtons.style.display="none";
            /*
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
            hiddenButtons.style.display="block";
            */
        }
        //check if highlighted selection is word, display buttons and post the hindiSelection to shabdkhosh
        else if(hindiSelection.match(wordRegex)){
            async function translateFunction(){
                const request=new Request("translationEndpoint", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ selection: hindiSelection, type: "word" })
                });
                let hindiResponse=await fetch(request);
                let hindiJSON=await hindiResponse.json();

                const numCols=hindiJSON.length;
                const gridContainer=document.getElementById('translatedWordPopUp');
                gridContainer.style.gridTemplateColumns=`repeat(${numCols}, 1fr)`;
                let translationData={};
                translationData['hindi']=hindiSelection;
                for(let prop in hindiJSON){
                    const numRows=hindiJSON[prop].length;
                    const subGrid=document.createElement('div');
                    subGrid.className='subGrid';
                    const gridEntry=document.createElement('div');
                    gridEntry.className='gridItem';
                    const pos=hindiJSON[prop]['pos'];
                    gridEntry.textContent=pos;
                    subGrid.appendChild(gridEntry);
                    translationData[pos]=''
                        for(word in hindiJSON[prop]['tr']){
                            const gridEntry=document.createElement('div');
                            gridEntry.className='gridItem';
                            gridEntry.textContent=hindiJSON[prop]['tr'][word]['tr'];
                            translationData[pos]=translationData[pos]+" "+hindiJSON[prop]['tr'][word]['tr'];
                            gridEntry.gridRow=word+2/word+3;
                            gridEntry.gridColumn=prop+1/prop+2;
                            subGrid.appendChild(gridEntry);
                        }
                        document.getElementById('translatedWordPopUp').appendChild(subGrid);
                    
                } 
                console.log("here is my JSON translationData", translationData);
                document.getElementById('translatedWordPopUp').style.display="grid";
                document.getElementById('translatedWordPopUp').style.margin="10px";
                document.getElementById('popUpContainer').style.display="block";
                const saveAllTranslations=document.getElementById('saveAllTranslations');  
                const translationsRequest=new Request("saveWordsEndpoint", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(translationData)
                });
                saveAllTranslations.onclick= async function(){
                    await fetch(translationsRequest);
                }

            }
            
            function romanizeFunction(){
                console.log('romanize function was called');
            }
            function saveWordFunction(){
                console.log('saveWord function called');
            }
            document.getElementById('translateButton').onclick=translateFunction;
            document.getElementById('romanizeButton').onclick=romanizeFunction;
            document.getElementById('saveWordButton').onclick=saveWordFunction;
            hiddenWordButtons.style.display="block";
            hiddenPhraseButtons.style.display="none";
        }
        else{
            hiddenWordButtons.style.display="none";
            hiddenPhraseButtons.style.display="none";
        }
    });
});

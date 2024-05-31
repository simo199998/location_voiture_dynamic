let btn_dispo=document.getElementById('btn-dispo');
let btn_cata=document.getElementById('btn-cata');
let matricule=document.getElementById('staticmatricule');
let prix=document.getElementById('staticprix');
let voiture_reser=document.getElementById('voitureselectionee');
let total=document.getElementById('total');
let datecharge=document.getElementById('encharge');
let datedepot=document.getElementById('depot');


function reserve(){
            /*let matricule_voiture=matricule.value*/
            let prix_voiture=prix.value
            return [/*matricule_voiture,*/prix_voiture];
}
function totaljours(){
            let encharge=datecharge.value
            let depot= datedepot.value
            number_jour=(new Date(depot)- new Date(encharge))/1000/60/60/24
            number_jour_int=Math.round(number_jour)
            return number_jour_int
}
let totaljour=totaljours()
let reser=reserve()
let prix_cars=reser[1]
let resultat=totaljour*prix_cars

total.value=resultat
console.log(resultat);
console.log(reser[0]);
console.log('hello');

function saveValue(id, val){
	// console.log("============", id, val)
    
    localStorage.setItem(id, val);// Every time user writing something, the localStorage's value will override . 
}

function getSavedValue(id){

    if (!localStorage.getItem(id)) {
        return "";// You can change this to your defualt value. 
    }

    return localStorage.getItem(id);
}

function clearValue(id) {
    localStorage.setItem(id, "");
}

function saveMultValue(id, val){
    var temp;
    
    if (typeof val === "object") {
        temp = val
    }
    else {
        temp = getMultSavedValue(id)
        temp.push(val)
    }
    
    localStorage.setItem(id, JSON.stringify(temp));// Every time user writing something, the localStorage's value will override . 

}

function getMultSavedValue(id){

    if (!localStorage.getItem(id)) {
        return [];// You can change this to your defualt value. 
    }
    // console.log("============", localStorage.getItem(id))

    return JSON.parse(localStorage.getItem(id));
}

function clearMultValue(id) {
    localStorage.setItem(id, JSON.stringify([]));
}

function clearStorage() {
    localStorage.clear();
}
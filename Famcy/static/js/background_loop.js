async function background_loop(url) {
	console.log("background_loop!!!!!!!!!!!!!!!!!")
    
    // Storing response
    const response = await fetch(url);
    const text = await response.json();

    console.log(text)
    
    // Storing data in form of JSON
    // var data = await response.json();
    
    // if (response) {
        // hideloader
    // }
}
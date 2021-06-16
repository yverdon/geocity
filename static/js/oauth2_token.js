// fetch('http://localhost:9095/oauth/token/', {
//     method: 'POST',
//     body: data,
//     headers: headers
// })
// .then(response => {
//     console.log(response)
//   })
//   .catch(err => {
//     console.log(err)
//   })

myHeaders = new Headers({
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "no-cache",
});

const getToken = async () => {
    const response = await fetch('http://localhost:9095/oauth/token/', {
        method: 'POST',
        headers: myHeaders,
        body: JSON.stringify({
            'client_id': 'As5Yn3R7Dcqt46C3r6iFc0uE0SVaHglAUld14UTw',
            'client_secret': 'RAt0oKycHuDB3dhiMiE845RzDyZlNrDs8YMFQXVZx4NqE8qwt5ew9L1FxIsXULWJa75SlrAXh5UXaFEkIRyt8yJimxkSMRBR860GaCabnFq3qfnI3r32GxXQbYxrlaSU',
            'code': '4FTPBnSpncz6VOpbS6kGtd6Nh49fLr',
            'redirect_uri': 'http://localhost:9095/token/',
            'grant_type': 'authorization-code'
        })
    })();
    console.log(response)
    const myJson = await response.json(); //extract JSON from the http response
    console.log(myJson)
}

// data: 'grant_type=authorization-code&code='+encodeURIComponent("3sQyANM9vUq9nGm4uNG41aYYWwm0ng")+'redirect_uri='+encodeURIComponent("http://localhost:9095/token/")+'&client_id='+encodeURIComponent("As5Yn3R7Dcqt46C3r6iFc0uE0SVaHglAUld14UTw")+'&client_secret='+encodeURIComponent("RAt0oKycHuDB3dhiMiE845RzDyZlNrDs8YMFQXVZx4NqE8qwt5ew9L1FxIsXULWJa75SlrAXh5UXaFEkIRyt8yJimxkSMRBR860GaCabnFq3qfnI3r32GxXQbYxrlaSU"),

getToken()
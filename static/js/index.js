const navLoggedInElement = document.querySelector("[data-nav-loggedIn]");
const navLoggedOutElement = document.querySelector("[data-nav-loggedOut]");

let me;

const getAccessToken = async () => {
    const resp = await axios.get('/refresh_token')
    return resp.data.token_type === 'bearer' ? resp.data.access_token : null
}

const getMe = async () => {
    const access_token = await getAccessToken()
    const resp = await axios.get('/users/me', {headers: {Authorization: `Bearer ${access_token}`}})
    return resp.data
}

const renderIsLoggedIn = async () => {
    try {
        me = await getMe()
        renderLoggedIn()
    } catch (e) {
        alert(e)
        me = null
        renderLoggedOut()
    }
}

const renderLoggedIn = () => {
    navLoggedOutElement.remove()
    navLoggedInElement.hidden = false
    const meElement = document.querySelector("[data-me]");
    meElement.innerText = me.username
}

const renderLoggedOut = () => {
    navLoggedInElement.remove()
    navLoggedOutElement.hidden = false
    const text = document.createElement("p")
    text.innerText="Du musst eingeloggt sein, um hier etwas zu tun"
    document.querySelector("body").appendChild(text)
}

const renderIndex = async () => {
    await renderIsLoggedIn()
}

renderIndex()

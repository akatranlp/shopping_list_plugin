import {user, axiosInstance, baseURL} from "./shopping_list_plugin_repo.js";

const productContainerElement = document.querySelector("[data-product-container]");
const createProductFormElement = document.querySelector("[data-create-product-form]");
const createProductNameElement = document.querySelector("[data-create-product-name]");
const createProductUrlElement = document.querySelector("[data-create-product-url]");
const createProductSelectElement = document.querySelector("[data-form-select]");
const formEdit = document.querySelector("[data-form-edit]")
const editProductName = document.querySelector("[data-edit-product-name]")
const editProductPicture = document.querySelector("[data-edit-product-url]")
const editProductUnit = document.querySelector("[data-edit-form-select]")

const getAllProducts = async () => {
    productContainerElement.innerHTML = ''
    const resp = await axiosInstance.get(baseURL + '/products')
    resp.data.forEach(product => {
        const productElement = document.createElement('div');
        if (product.pic_url) {
            const imgElement = document.createElement('img')
            imgElement.style.maxHeight = "80px"
            imgElement.style.maxWidth = "80px"
            imgElement.src = product.pic_url
            productElement.appendChild(imgElement)
        }

        const table = document.createElement("table")
        const thead = document.createElement("thead")
        const tbody = document.createElement("tbody")
        const tr = document.createElement("tr")

        const elementName = document.createElement('td')
        elementName.innerText = product.name
        tr.appendChild(elementName)

        const divide = document.createElement('td')
        tr.appendChild(divide)

        const elementType = document.createElement('td')
        elementType.innerText = product.unit_type
        tr.appendChild(elementType)

        table.appendChild(thead)
        table.appendChild(tbody)
        tbody.appendChild(tr)
        productElement.appendChild(table)

        const changeBtnElement = document.createElement('button')
        changeBtnElement.innerText = 'Bearbeiten'
        changeBtnElement.className = "btn btn-success mr-sm-2"
        changeBtnElement.setAttribute("data-toggle", "modal")
        changeBtnElement.setAttribute("data-target", "#editModal")
        changeBtnElement.addEventListener('click', async () => {

            editProductName.value = product.name
            editProductPicture.value = product.pic_url

            formEdit.addEventListener("submit", async (event) => {

                const name = editProductName.value
                const pic_url = editProductPicture.value
                const unit_id = editProductUnit.value
                const data = {name, pic_url, unit_id}

                try {
                    await axiosInstance.put(`${baseURL}/products/${product.uuid}`, data)
                    window.location = "/plugin/shopping_list_plugin/product"
                    editProductName.value = ''
                    editProductPicture.value = ''
                } catch (e) {
                    openErrorAlert("Es ist ein Fehler aufgetreten", e)
                }
            })
        })
        productElement.appendChild(changeBtnElement)

        const deleteBtnElement = document.createElement('button')
        deleteBtnElement.innerText = 'Löschen'
        deleteBtnElement.className = "btn btn-danger mr-sm-2"
        deleteBtnElement.addEventListener('click', async () => {
            try {
                await axiosInstance.delete(`${baseURL}/products/${product.uuid}`)
                await getAllProducts()
            } catch (e) {
                openErrorAlert("Es ist ein Fehler aufgetreten", e)
            }
        })
        productElement.appendChild(deleteBtnElement)
        const brk = document.createElement("hr")
        productElement.appendChild(brk)
        productContainerElement.appendChild(productElement);
    })
}


const addOptions = async () => {
    const resp = await axiosInstance.get(baseURL + '/units')
    resp.data.forEach(unit => {
        const optionElement = document.createElement('option');
        optionElement.innerText = unit.unit
        optionElement.value = unit.id
        let cln = optionElement.cloneNode(true)
        createProductSelectElement.appendChild(optionElement)
        editProductUnit.appendChild(cln)
    })
}


const init = async () => {
    await addOptions()

    createProductFormElement.addEventListener('submit', async e => {
        e.preventDefault()
        const unit_id = createProductSelectElement.value
        const name = createProductNameElement.value
        const pic_url = createProductUrlElement.value

        const data = {name, unit_id}
        if (pic_url)
            data.pic_url = pic_url

        try {
            await axiosInstance.post(baseURL + '/products', data)
            window.location = "/plugin/shopping_list_plugin/product"
            createProductNameElement.value = ''
            createProductUrlElement.value = ''
        } catch (e) {
            openErrorAlert(e.response.data.detail, e)
        }
    })

    await getAllProducts()
}

const openErrorAlert = (text, e) => {
    errorAlert.className = "alert alert-danger p-1"
    if (e !== null) {
        errorAlert.innerText = text + ": " + e.response.status + " - " + e.response.statusText
    } else {
        errorAlert.innerText = text
    }
    errorAlert.removeAttribute("hidden")
}

init()


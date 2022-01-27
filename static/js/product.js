import {user, axiosInstance, baseURL} from "./shopping_list_plugin_repo.js";

const productContainerElement = document.querySelector("[data-product-container]");

const createProductFormElement = document.querySelector("[data-create-product-form]");
const createProductNameElement = document.querySelector("[data-create-product-name]");
const createProductUrlElement = document.querySelector("[data-create-product-url]");
const createProductSelectElement = document.querySelector("[data-form-select]");

const getAllProducts = async () => {
    productContainerElement.innerHTML = ''
    const resp = await axiosInstance.get(baseURL + '/products')
    resp.data.forEach(product => {
        const productElement = document.createElement('div');
        if (product.pic_url) {
            const imgElement = document.createElement('img')
            imgElement.src = product.pic_url
            productElement.appendChild(imgElement)
        }

        {
            const tempElement = document.createElement('p')
            tempElement.innerText = product.name
            productElement.appendChild(tempElement)
        }
        {
            const tempElement = document.createElement('p')
            tempElement.innerText = product.unit_type
            productElement.appendChild(tempElement)
        }

        const changeBtnElement = document.createElement('button')
        changeBtnElement.innerText = 'Change'
        changeBtnElement.addEventListener('click', async () => {
            // TODO open form oder so

            const name = 'TODO'
            const pic_url = ''
            const unit_id = 1
            const data = {name, pic_url, unit_id}

            try {
                await axiosInstance.put(`${baseURL}/products/${product.uuid}`, data)
                await getAllProducts()
            } catch (e) {
                alert(e)
            }
        })
        productElement.appendChild(changeBtnElement)

        const deleteBtnElement = document.createElement('button')
        deleteBtnElement.innerText = 'Delete'
        deleteBtnElement.addEventListener('click', async () => {
            try {
                await axiosInstance.delete(`${baseURL}/products/${product.uuid}`)
                await getAllProducts()
            } catch (e) {
                alert(e)
            }
        })
        productElement.appendChild(deleteBtnElement)

        productContainerElement.appendChild(productElement);
    })
}


const addOptions = async () => {
    const resp = await axiosInstance.get(baseURL + '/units')
    resp.data.forEach(unit => {
        const optionElement = document.createElement('option');
        optionElement.innerText=unit.unit
        optionElement.value=unit.id
        createProductSelectElement.appendChild(optionElement)
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
            await getAllProducts()
            createProductNameElement.value = ''
            createProductUrlElement.value = ''
        } catch (e) {
            alert(e.response.data.detail)
        }
    })

    await getAllProducts()
}

init()

import {user, axiosInstance, baseURL} from "./shopping_list_plugin_repo.js";

const listContainerElement = document.querySelector("[data-list-container]");

const createListFormElement = document.querySelector("[data-create-list-form]");
const createListNameElement = document.querySelector("[data-create-list-name]");

const getAllLists = async () => {
    listContainerElement.innerHTML = ''
    const resp = await axiosInstance.get(baseURL + '/shoppingLists')
    resp.data.forEach(list => {
        const listContainer = document.createElement('div')
        listContainer.className = 'border border-primary'

        const listNameElement = document.createElement('div')
        listNameElement.innerText = list.name
        listContainer.appendChild(listNameElement)

        const listChangeBtnElement = document.createElement('button')
        listChangeBtnElement.className = 'btn btn-warning text-white mr-sm-2'
        listChangeBtnElement.innerText = 'Change'
        listContainer.appendChild(listChangeBtnElement)

        listChangeBtnElement.addEventListener('click', async () => {
            // TODO wieder irgendwas öffnen zum eingeben
            try {
                const name = 'TODO'
                await axiosInstance.put(`${baseURL}/shoppingLists/${list.uuid}`, {name})
                await getAllLists()
            } catch (e) {
                alert(e)
            }
        })

        const listDeleteBtnElement = document.createElement('button')
        listDeleteBtnElement.className = 'btn btn-danger text-white mr-sm-2'
        listDeleteBtnElement.innerText = 'Delete'
        listContainer.appendChild(listDeleteBtnElement)

        listDeleteBtnElement.addEventListener('click', async () => {
            try {
                await axiosInstance.delete(`${baseURL}/shoppingLists/${list.uuid}`)
                await getAllLists()
            } catch (e) {
                alert(e)
            }
        })

        listContainer.appendChild(getListEntriesContainer(list))

        listContainerElement.appendChild(listContainer)
    })
}


const getListEntriesContainer = (list) => {
    const listEntriesContainer = document.createElement('div');
    listEntriesContainer.className = 'border border-secondary'

    list.entries.forEach(entry => {
        listEntriesContainer.appendChild(getEntryContainer(list, entry));
    })

    const addEntryBtnElement = document.createElement('button')
    addEntryBtnElement.className = 'btn btn-primary text-white mr-sm-2'
    addEntryBtnElement.innerText = '+'
    listEntriesContainer.appendChild(addEntryBtnElement)

    addEntryBtnElement.addEventListener('click', async () => {
        const createEntryFormElement = document.createElement('form')
        createEntryFormElement.action = ''
        createEntryFormElement.method = 'post'

        const createEntryProductSelectElement = await getSelectProductContainer()
        createEntryFormElement.appendChild(createEntryProductSelectElement)

        const createEntryProductAmountElement = document.createElement('input')
        createEntryProductAmountElement.type = 'number'
        createEntryFormElement.appendChild(createEntryProductAmountElement)

        const createEntryProductBtnElement = document.createElement('input')
        createEntryProductBtnElement.type = 'submit'
        createEntryProductBtnElement.value = 'Add Entry'
        createEntryFormElement.appendChild(createEntryProductBtnElement)

        createEntryFormElement.addEventListener('submit', async e => {
            e.preventDefault()
            const product_uuid = createEntryProductSelectElement.value
            const amount = createEntryProductAmountElement.value

            try {
                const resp = await axiosInstance.post(`${baseURL}/shoppingLists/${list.uuid}/entries`, {
                    product_uuid,
                    amount
                })
                listEntriesContainer.insertBefore(getEntryContainer(list, resp.data), createEntryFormElement)
                createEntryFormElement.remove()
            } catch (e) {
                alert(e)
            }
        })

        const createEntryProductBtnCancelElement = document.createElement('button')
        createEntryProductBtnCancelElement.innerText = 'Cancel'
        createEntryFormElement.appendChild(createEntryProductBtnCancelElement)

        createEntryProductBtnCancelElement.addEventListener('click', () => {
            createEntryFormElement.remove()
        })

        listEntriesContainer.insertBefore(createEntryFormElement, addEntryBtnElement)
    })

    return listEntriesContainer
}

const getEntryContainer = (list, entry) => {
    const entryElement = document.createElement('div')
    entryElement.className = "border border-danger"

    {
        const tempElement = document.createElement('p')
        tempElement.innerText = entry.product_name
        entryElement.appendChild(tempElement)
    }

    if (entry.product_pic_url) {
        const entryImgElement = document.createElement('img')
        entryImgElement.src = entry.product_pic_url
        entryElement.appendChild(entryImgElement)
    }

    const entryAmountElement = document.createElement('p')
    entryAmountElement.innerText = entry.amount
    entryElement.appendChild(entryAmountElement)

    {
        const tempElement = document.createElement('p')
        tempElement.innerText = entry.product_unit_type
        entryElement.appendChild(tempElement)
    }

    const entryChangeBtnElement = document.createElement('button')
    entryChangeBtnElement.className = 'btn btn-warning text-white mr-sm-2'
    entryChangeBtnElement.innerText = 'Change'
    entryElement.appendChild(entryChangeBtnElement)

    entryChangeBtnElement.addEventListener('click', async () => {
        alert(entry.uuid)
    })

    const entryDeleteBtnElement = document.createElement('button')
    entryDeleteBtnElement.className = 'btn btn-danger text-white mr-sm-2'
    entryDeleteBtnElement.innerText = 'Delete'
    entryElement.appendChild(entryDeleteBtnElement)

    entryDeleteBtnElement.addEventListener('click', async () => {
        try {
            await axiosInstance.delete(`${baseURL}/shoppingLists/${list.uuid}/entries/${entry.uuid}`)
            entryElement.remove()
        } catch (e) {
            alert(e)
        }
    })
    return entryElement
}

const getSelectProductContainer = async () => {
    const resp = await axiosInstance.get(baseURL + '/products')

    const selectElement = document.createElement('select')
    resp.data.forEach(product => {
        const optionElement = document.createElement('option')
        optionElement.innerText = product.name
        optionElement.value = product.uuid
        selectElement.appendChild(optionElement)
    })
    return selectElement
}


const init = async () => {
    await getAllLists()

    createListFormElement.addEventListener('submit', async e => {
        e.preventDefault()

        const name = createListNameElement.value
        try {
            await axiosInstance.post(`${baseURL}/shoppingLists`, {name})
            await getAllLists()
            createListNameElement.value = ''
        } catch (e) {
            alert(e)
        }
    })
}

init()

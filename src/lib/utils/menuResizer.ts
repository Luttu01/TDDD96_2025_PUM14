
export function adjustMenu() {
    const MORE = document.getElementById("More") as HTMLDivElement;
    const MENU = document.getElementById("Filtermenu") as HTMLDivElement;
    const MORE_MENU = document.getElementById("More-List");

    if(MENU == null || MORE_MENU == null) return;
    const menuItems = Array.from(MENU.children);

    let width = MENU.clientWidth;
    let movedWidth = 0;
    let itemsInMotion: Element[] = [];
    

    menuItems.forEach((item) => {
        movedWidth += (item as HTMLElement).offsetWidth;
        const child = document.getElementById(item.id);
        if(movedWidth > width) {
            itemsInMotion.push(item);
            console.log(item.id);
            if(child != null) child.style.display = "none";
        } else {
            if(child != null) {
                if(child.id == "DatumDiv") {
                    child.style.display = "Flex";
                } else {
                    child.style.display = "block";
                }
            }
        }
    });
    MORE_MENU.innerHTML = "";
    itemsInMotion.forEach((item) => {
        const newItem = document.createElement("li");
        newItem.textContent = item.textContent;
        MORE_MENU.appendChild(newItem);
    })
    // MENU -> Children
    // MORE_MENU -> Rest of Children
    // MENU + MORE_MENU = All children
    
    if(itemsInMotion.length > 0) {
        MORE.style.display = "block";
    } else {
        MORE.style.display = "none";
    }
 }
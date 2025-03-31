const MENU = document.getElementById("Filtermenu") as HTMLDivElement;
const MORE = document.getElementById("More") as HTMLDivElement;
const MORE_MENU = document.getElementById("More-List");

function adjustMenu() {
    if(MENU == null) return;
    const menuItems = Array.from(MENU.children);

    let width = MENU.clientWidth;
    let itemsMoved = [];
    let movedWidth = 0;

    menuItems.forEach((item) => {
        movedWidth += (item as HTMLElement).offsetWidth;
        if(movedWidth > width) {
            itemsMoved.push(item);
        }
    });
    if(itemsMoved.length > 0) {
        MORE.style.display = "block";
    } else {
        MORE.style.display = "none";
    }
 }

window.addEventListener("resize", adjustMenu);
window.addEventListener("load", adjustMenu);
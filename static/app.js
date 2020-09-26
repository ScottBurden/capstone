const updateGrade = document.getElementsByClassName("update")
const loginForm = document.getElementById("username")

if (loginForm){
    loginForm.focus();
}
if (updateGrade){
    for (let grade of updateGrade){
        grade.addEventListener("click", (e) => {
            e.preventDefault();
            let form = e.target.parentElement;
            let els = form.children;
            for (let el in els){
                el.style.visibility="visible";
                e.target.nextElementSibling.focus();
            }
        })
    }
}
const btn = document.querySelectorAll("a")

for (let b of btn){
    b.addEventListener("click", (e) => {
	let hw = e.target.getAttribute("id");
	let idHw = hw.split("-");
	let complete = document.getElementById(idHw[1])
	complete.setAttribute("class","btn btn-success")
	e.target.setAttribute("class", "btn btn-success")
    })}
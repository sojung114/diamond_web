function analysis_start() {
  fetch("http://localhost:5000/final", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((json) => {
      alert("123");
    });
}
function test() {
  fetch("http://localhost:5000/final", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((json) => {
      alert("123");
    });
}

// fetch("http://127.0.0.1:5500/templates/", {
//   method: "GET",
//   headers: {
//     "Content-Type": "application/json",
//   },
// })
//   .then((response) => response.json())
//   .then((data) => {
//     Alert("123");
//     // document.getElementById("user_name").innerHTML = data[0].M_name;
//     // document.getElementById("user_dept").innerHTML = data[0].dept;
//   });

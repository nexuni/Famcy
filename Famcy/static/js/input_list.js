function generate_list(list_id) {
  var x, i, j, l, ll, selElmnt, a, b, c, d, temp;

  x = document.getElementById(list_id+"_inputList");      // div.inputList
  // console.log(x)

  selElmnt = x.getElementsByTagName("select")[0];         // div.select
  // console.log(selElmnt.selectedIndex)

  ll = selElmnt.length;

  /*for each element, create a new DIV that will act as the selected item:*/
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x.appendChild(a);

  /*for each element, create a new DIV that will contain the option list:*/
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");

  // console.log(selElmnt.options[selElmnt.selectedIndex], selElmnt.options[selElmnt.selectedIndex].getAttribute("name"))
  d = document.createElement("INPUT");
  d.setAttribute("id", selElmnt.options[selElmnt.selectedIndex].getAttribute("name"));
  d.setAttribute("type", "hidden");
  d.setAttribute("name", selElmnt.options[selElmnt.selectedIndex].getAttribute("name"));
  b.appendChild(d);

    for (j = 1; j < ll; j++) {
      /*for each option in the original select element,
      create a new DIV that will act as an option item:*/
      c = document.createElement("DIV");
      c.innerHTML += selElmnt.options[j].innerHTML;

      c.addEventListener("click", function(e) {
          /*when an item is clicked, update the original select box,
          and the selected item:*/
          var y, i, k, s, h, sl, yl;
          s = this.parentNode.parentNode.getElementsByTagName("select")[0];
          // console.log(s, s.options)
          sl = s.length;
          h = this.parentNode.previousSibling;
          
          for (i = 0; i < sl; i++) {
            if (s.options[i].innerHTML == this.innerHTML) {
              s.selectedIndex = i;
              h.innerHTML = this.innerHTML;
              document.getElementById(s.options[i].getAttribute("name")).setAttribute("value", this.innerHTML)

              if (selElmnt.getAttribute("after_action").includes("save")) {
                saveValue(s.options[s.selectedIndex].getAttribute("name"), this.innerHTML)
              }

              // if (s.getAttribute("selected_action") == "True" || s.getAttribute("selected_action")) {
                // Sijax.request('famcy_submission_handler', [submission_obj_id, {"list_value": this.innerHTML, "list_flag": "True"}]);
              // }

              y = this.parentNode.getElementsByClassName("same-as-selected");
              yl = y.length;
              for (k = 0; k < yl; k++) {
                y[k].removeAttribute("class");
              }
              this.setAttribute("class", "same-as-selected");
              break;
            }
          }
          h.click();
      });
      b.appendChild(c);
    }
    x.appendChild(b);
    a.addEventListener("click", function(e) {
      /*when the select box is clicked, close any other select boxes,
      and open/close the current select box:*/
      e.stopPropagation();
      closeAllSelect(this);
      this.nextSibling.classList.toggle("select-hide");
      this.classList.toggle("select-arrow-active");
    });

    if (selElmnt.getAttribute("after_action").includes("save")) {

      temp = getSavedValue(selElmnt.options[selElmnt.selectedIndex].getAttribute("name"))

      if (temp == "") {
        temp = "---"
      }
      document.getElementById(selElmnt.options[selElmnt.selectedIndex].getAttribute("name")).setAttribute("value", temp)
      a.innerHTML = temp
    }
  // }
  function closeAllSelect(elmnt) {
    /*a function that will close all select boxes in the document,
    except the current select box:*/
    var x, y, i, xl, yl, arrNo = [];
    x = document.getElementsByClassName("select-items");
    y = document.getElementsByClassName("select-selected");
    xl = x.length;
    yl = y.length;
    for (i = 0; i < yl; i++) {
      if (elmnt == y[i]) {
        arrNo.push(i)
      } else {
        y[i].classList.remove("select-arrow-active");
      }
    }
    for (i = 0; i < xl; i++) {
      if (arrNo.indexOf(i)) {
        x[i].classList.add("select-hide");
      }
    }
  }
  /*if the user clicks anywhere outside the select box,
  then close all select boxes:*/
  document.addEventListener("click", closeAllSelect);
}


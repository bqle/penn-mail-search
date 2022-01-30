'use strict';
import React, {useState, useEffect} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import $ from 'jquery';

const CollegeNameVariations = ['college of arts & sciences']
const EngineeringNameVariations = ['engineering & applied science undergrad', 
                    'engineering & applied science masters',
                    'engineering & applied science phd'
                ]
const WhartonNameVariations = ['wharton undergraduate', 'wharton graduate']
const NursingNameVariations = ['nursing undergraduate']

var schoolChoice = "Any";

function OptionField(props) {
  return (
    <div className={`box ${props.isActive ? "active" : "inactive"}`} 
    onClick={() => {props.changeCursorIndex();props.copyToClipBoard();}}
    onMouseEnter={() => props.changeCursorIndex()}
    >
      <div className={"name"}>{props.name}</div>
      <div className={"sub"}>{props.email}</div>
      <div className={"sub"}>{props.school + " - " + props.major}</div>
    </div >
  )
}

function SearchBar() {
  function handleKeyDown(e) {
    if (e.code === "ArrowUp" || e.code === "ArrowDown") {
      e.preventDefault();
    }
  }

  return (
    <div className="search-bar">
    <input type="text" id="searchText" className="search-bar--text" autoComplete="off" onKeyDown={handleKeyDown} autoFocus={true}></input>
    <div className="custom-select">
      <select id="school-select">
        <option value="0">School</option>
        <option value="1">Any</option>
        <option value="2">College</option>
        <option value="3">Engineering</option>
        <option value="4">Nursing</option>
        <option value="5">Wharton</option>
        </select>
      </div>
    </div>
  ) 
}

function ResultList(props) {
 
  // suggestions has structure [{name: , id: , email: , school: , major: }, ...]
  const [cursor, setCursor] = useState(0);
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    function fetchSuggestions() {
      let school = 0;
      switch(schoolChoice) {
        case "Any": school = 0 ; break;
        case "College": school = 1; break;
        case "Engineering": school = 2; break;
        case "Nursing": school = 3; break;
        case "Wharton": school = 4; break;
      }
      let searchText = encodeURI(document.getElementById("searchText").value);
      let url = 'http://localhost:5000/search?name='+searchText+'&school='+school;
      console.log(url);

      fetch (url)
      .then(res => res.json())
      .then(
        (result) => {
          console.log("fetched...");
          console.log(result)
          setIsLoaded(true);
          for (let i = 0 ; i < result.length; i++) {
            result[i].id = i;
            if (CollegeNameVariations.includes(result[i]["School"])) {
              result[i]["School"] = "College";
            } else if (EngineeringNameVariations.includes(result[i]["School"])) {
              result[i]["School"] = "Engineering";
            } else if (NursingNameVariations.includes(result[i]["School"])) {
              result[i]["School"] = "Nursing";
            } else if (WhartonNameVariations.includes(result[i]["School"])) {
              result[i]["School"] = "Wharton";
            }
          }
          setSuggestions(result);
          setCursor(0);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
          setSuggestions([]);
        }
      )
    }

    function handleKeyDown(e) {
      if (e.code === "ArrowUp" && cursor > 0) {
        setCursor(cursor - 1);
      } else if (e.code === "ArrowDown" && cursor < suggestions.length - 1) {
        setCursor(cursor + 1);
      } else if (e.code === "Enter") {
        console.log(suggestions[cursor]);
        if (suggestions[cursor] !== undefined) {
          navigator.clipboard.writeText(suggestions[cursor]['Email']);
        }
      }
    }
    
    document.addEventListener("keydown", handleKeyDown);
    // on typing a name or selecting a school, a search is made
    $('#searchText').on('input', fetchSuggestions);
    $('.select-items').on('click', fetchSuggestions);

    return function cleanup() {
      document.removeEventListener("keydown", handleKeyDown);
      $('#searchText').off('input');
      $('.select-items').off('click');
    };
  }, [cursor, suggestions]);

  function changeCursorIndex(index) {
    setCursor(index);
  }

  function copyToClipBoard() {
    navigator.clipboard.writeText(suggestions[cursor]['Email']);
  }

  if (error) {
    return <div className={"box box-loading"}>Error : {error.message}</div>
  } else if (!isLoaded) {
    return <div className={"box box-loading"}>Loading...</div> 
  } else {
    var items = suggestions.map((person) => {
                return <OptionField key={person['id']} email={person['Email']}
                    school={person['School']}
                    major={person['Major']}
                    name={person['Name']}
                    isActive={person['id']=== cursor}
                    changeCursorIndex={() => changeCursorIndex(person['id'])}
                    copyToClipBoard={() => copyToClipBoard()}
                    >
                  </OptionField>;
                })

    return (
      <ul>{items}</ul>
    )
  }
}

// ========================================


const app = ReactDOM.render(<div><SearchBar /><ResultList /></div>, document.getElementById("root"));

function makeSearchTextFieldActive(e) {
  let searchTextfield = document.getElementById('searchText');
  searchTextfield.focus();
  
}

document.addEventListener("keydown", makeSearchTextFieldActive);




/* For Custom Select Component ============== */
var x, i, j, l, ll, selElmnt, a, b, c;
/* Look for any elements with the class "custom-select": */
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  /* For each element, create a new DIV that will act as the selected item: */
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /* For each element, create a new DIV that will contain the option list: */
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < ll; j++) {
    /* For each option in the original select element,
    create a new DIV that will act as an option item: */
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.setAttribute("class", "select-item")
    c.addEventListener("click", function(e) {
        /* When an item is clicked, update the original select box,
        and the selected item: */
        var y, i, k, s, h, sl, yl;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        sl = s.length;
        h = this.parentNode.previousSibling;
        for (i = 0; i < sl; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            yl = y.length;
            for (k = 0; k < yl; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        schoolChoice = this.innerHTML;
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
    /* When the select box is clicked, close any other select boxes,
    and open/close the current select box: */
    e.stopPropagation();
    closeAllSelect(this);
    this.nextSibling.classList.toggle("select-hide");
    this.classList.toggle("select-arrow-active");
  });
}

function closeAllSelect(elmnt) {
  /* A function that will close all select boxes in the document,
  except the current select box: */
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

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);


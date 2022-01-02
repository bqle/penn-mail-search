'use strict';
import React, {useState, useEffect} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import $ from 'jquery';


function OptionField(props) {
  
  return (
    <div className={`box ${props.isActive ? "active" : "inactive"}`}>
      <div className={"name"}>{props.name}</div>
      <div className={"sub"}>{props.email} {props.school} {props.major}</div>
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
    <input type="text" id="searchBar" className={"search-bar"} autoComplete="off" onKeyDown={handleKeyDown} autoFocus={true}></input>
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
      fetch ('https://jsonkeeper.com/b/JOM3')
      .then(res => res.json())
      .then(
        (result) => {
          console.log("fetched...");
          setIsLoaded(true);
          for (let i = 0 ; i < result.length; i++) {
            result[i].id = i;
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
        console.log('clipped');
        navigator.clipboard.writeText(suggestions[cursor].email);
      }
    }
    
    document.addEventListener("keydown", handleKeyDown);
    $('#searchBar').on('input', fetchSuggestions);

    return function cleanup() {
      document.removeEventListener("keydown", handleKeyDown);
      $('#searchBar').off('input');
    };
  }, [cursor, suggestions]);

  if (error) {
    return <div className={"box"}>Error : {error.message}</div>
  } else if (!isLoaded) {
    return <div className={"box"}>Loading...</div> 
  } else {
    var items = suggestions.map((person) => {
                return <OptionField key={person.id} email={person.email}
                    school={person.school}
                    major={person.major}
                    name={person.name}
                    isActive={person.id === cursor}
                    >
                  </OptionField>;
                })

    return (
      <ul>{items}</ul>
    )
  }
}

// ========================================


const suggestions = [];
for (let i = 0 ; i < 6; i++) {
  suggestions.push({name: "Ben Le", email: "bqle@seas.upenn.edu" + i, school: "SEAS", major: "CS", id: i});
}

ReactDOM.render(<div><SearchBar /><ResultList /></div>, document.getElementById("root"));

function makeSearchBarActive(e) {
  let searchBar = document.getElementById('searchBar');
  searchBar.focus();
  
}

document.addEventListener("keydown", makeSearchBarActive);
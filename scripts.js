// scripts.js
function registerUser() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: username, password: password})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function linkPartner() {
    var userID = document.getElementById("userID").value;
    var partnerID = document.getElementById("partnerID").value;

    fetch('/link', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({user_id: userID, partner_id: partnerID})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getRelationshipInfo(uniqueID) {
    fetch('/relationship/' + uniqueID)
    .then(response => response.json())
    .then(data => {
        var relationshipData = document.getElementById("relationshipData");
        relationshipData.innerHTML = '';
        data.relationships.forEach(function(relationship) {
            var p = document.createElement("p");
            p.textContent = "Relationship ID: " + relationship.RelationshipID + ", Start Date: " + relationship.StartDate + ", Milestones: " + relationship.Milestones;
            relationshipData.appendChild(p);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Example usage:
// getRelationshipInfo('your_unique_id');

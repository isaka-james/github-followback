const githubFields = document.getElementById("github-fields");

function toggleGithubFields(state="toggle"){
	if (state=="toggle"){
		if (githubFields.classList.contains("hidden")) {
			githubFields.classList.remove("hidden");
			githubFields.classList.add("block");
		} else {
			githubFields.classList.add("hidden");
			githubFields.classList.remove("block");
		}
	}else if(state="close"){
		if (githubFields.classList.contains("hidden")) {
			
		} else {
			githubFields.classList.add("hidden");
			githubFields.classList.remove("block");
		}
	}
}

document.getElementById("unfollowToggleText").addEventListener("click", function() {
	toggleGithubFields();
});

document.getElementById("checkBtn").addEventListener("click", function () {
    const username = document.getElementById("username").value.trim();
    const key = document.getElementById("key").value.trim();
    const resultDiv = document.getElementById("result");
    const loadingDiv = document.getElementById("loading");
    const profilePictureDiv = document.getElementById("profilePicture");
    const userAvatar = document.getElementById("userAvatar");
    const userName = document.getElementById("userName");

    if (!username) {
        alert("Please enter a username.");
        return;
    }


    const unfollowNotFollowedBack = document.getElementById('unfollowNotFollowedBack').checked;
    const unfollowAllUsers = document.getElementById('unfollowAllUsers').checked;

    // Store states in variables
    const unfollowNotFollowedBackValue = unfollowNotFollowedBack; // True or False
    const unfollowAllUsersValue = unfollowAllUsers; // True or False


    // Encode key or use "Empty" message if not filled
    const encodedKey = key ? btoa(key) : btoa("Empty");

    // Show loading animation
    loadingDiv.classList.add("active");
    resultDiv.innerHTML = "";
    profilePictureDiv.classList.add("hidden"); // Hide profile picture initially

fetch('/github', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: username,
        key: encodedKey,
		unfollow_not_followback:unfollowNotFollowedBackValue,
		unfollow_all_users:unfollowAllUsersValue 
    })
})
.then(response => {
    loadingDiv.classList.remove("active");
	toggleGithubFields("close");

    // Check if the response is okay
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }

    return response.json();
})
.then(data => {
    // Log the received data for debugging
    console.log("Response Data:", data);

    // Handle errors based on the response
    switch (data.error) {
        case "12":
            resultDiv.innerHTML = `
                <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md">
                    <p class="font-semibold">Invalid GitHub Key. Please check your key and try again.</p>
                </div>
            `;
            return;

        case "13":
            resultDiv.innerHTML = `
                <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md">
                    <p class="font-semibold">Error decoding GitHub Key. Please ensure it is valid.</p>
                </div>
            `;
            return;

        case "14":
            resultDiv.innerHTML = `
                <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md">
                    <p class="font-semibold">Provided GitHub username does not exist. Please check the username.</p>
                </div>
            `;
            return;

        case "15":
            resultDiv.innerHTML = `
                <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md">
                    <p class="font-semibold">Fill both fields Inputs.</p>
                </div>
            `;
            return;

        default:
            // Proceed with updating the profile picture and username if no errors
            userAvatar.src = `https://github.com/${username}.png`;
            userName.textContent = `@${username}`;
            profilePictureDiv.classList.remove("hidden");

            // Display the results
            resultDiv.innerHTML = `
                <div class="p-6 bg-white shadow-lg rounded-lg">
                    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Results for <span class="text-blue-500">@${username}</span></h2>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
                        <div class="p-4 bg-blue-100 rounded-lg border border-blue-300 text-center">
                            <h3 class="font-bold text-lg">Followers</h3>
                            <p class="text-2xl text-blue-600">${data.followers_count}</p>
                        </div>
                        <div class="p-4 bg-green-100 rounded-lg border border-green-300 text-center">
                            <h3 class="font-bold text-lg">Following</h3>
                            <p class="text-2xl text-green-600">${data.following_count}</p>
                        </div>
                    </div>

                    <h3 class="mt-4 font-bold text-xl">Not Followed Back:</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                        ${data.not_following_back.map(name => `
                            <div class="bg-gray-100 rounded-lg p-4 shadow hover:shadow-md transition-shadow duration-200">
                                <div class="flex flex-col items-center">
                                    <img src="https://github.com/${name.replace('@', '')}.png" alt="${name}" class="w-16 h-16 rounded-full mb-2">
                                    <span class="font-bold">${name}</span>
                                    <a href="https://github.com/${name.replace('@', '')}" target="_blank" class="text-blue-500 hover:underline mt-2">View Profile</a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    
                    <h3 class="mt-4 font-bold text-xl">Not Following Me:</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                        ${data.not_followed_by_me.map(name => `
                            <div class="bg-gray-100 rounded-lg p-4 shadow hover:shadow-md transition-shadow duration-200">
                                <div class="flex flex-col items-center">
                                    <img src="https://github.com/${name.replace('@', '')}.png" alt="${name}" class="w-16 h-16 rounded-full mb-2">
                                    <span class="font-bold">${name}</span>
                                    <a href="https://github.com/${name.replace('@', '')}" target="_blank" class="text-blue-500 hover:underline mt-2">View Profile</a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            return;
    }
})
.catch(error => {
    loadingDiv.classList.remove("active");
    console.error("Fetch Error:", error);

    // Update the result div to inform the user about the scraping issue
    resultDiv.innerHTML = `
        <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md">
            <p class="font-semibold text-lg">Whoa! Looks like you have a massive follower or following count, and we’re hitting Vercel's 10-second scrape limit! 😅</p>
            <p>Sorry, we couldn’t fetch all your data from GitHub in time. If you'd consider sponsoring, we could scrape faster and go deeper into your GitHub world!</p>
            <p>If you've got a buddy with fewer followers, feel free to test their account and see it in action! 😎</p>
            <p>If you have a GitHub key, please input it and try again.</p>
        </div>
    `;
});



});


document.getElementById("checkBtn").addEventListener("click", function () {
    const username = document.getElementById("username").value.trim();
    const resultDiv = document.getElementById("result");
    const loadingDiv = document.getElementById("loading");
    const profilePictureDiv = document.getElementById("profilePicture");
    const userAvatar = document.getElementById("userAvatar");
    const userName = document.getElementById("userName");

    if (!username) {
        alert("Please enter a username.");
        return;
    }

    // Show loading animation
    loadingDiv.classList.add("active");
    resultDiv.innerHTML = "";
    profilePictureDiv.classList.add("hidden"); // Hide profile picture initially

    fetch(`/github?username=${username}`)
        .then(response => {
            loadingDiv.classList.remove("active");
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            if (data.status === "failed") {
                resultDiv.innerHTML = `
    <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md">
        <p class="font-semibold">Oops! It seems we couldn't find any GitHub account under the username <strong>${username}</strong>.</p>
        <p>Please double-check the spelling or try another username. If you need help, feel free to reach out!</p>
    </div>
`;

                return;
            }

            // Update the profile picture and username
            userAvatar.src = `https://github.com/${username}.png`;
            userName.textContent = `@${username}`;
            profilePictureDiv.classList.remove("hidden");

            // Dynamically render the results in the existing structure
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

        })
        .catch(error => {
            loadingDiv.classList.remove("active");
            //resultDiv.innerHTML = `<p class="text-red-500">Error: ${error.message}</p>`;
resultDiv.innerHTML = `
    <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md">
        <p class="font-semibold text-lg">Whoa! Looks like you have a massive follower or following count, and we’re hitting Vercel's 10-second scrape limit! 😅</p>
        <p>Sorry, we couldn’t fetch all your data from GitHub in time. If you'd consider sponsoring, we could scrape faster and go deeper into your GitHub world!</p>
        <p>If you've got a buddy with fewer followers, feel free to test their account and see it in action! 😎</p>
    </div>
`;

        });
});


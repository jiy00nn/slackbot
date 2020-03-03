

headers = {
    "Authorization": "Bearer af4e68fdefc8ed75643ff3604bde4f1de54c77ce",
    "Content-Type": "application/json", 
    "Accept": "application/vnd.github.inertia-preview+json"
    }

query = {
    user(login: "jiyoonbak"){
        repositories(last: 100){
            totalCount nodes{
                name defaultBranchRef{
                    target{
                        ...on Commit{
                            history(since: "2020-02-16T09:00:00+00:00"){
                                totalCount
                            }
                        }
                    }
                }
            }
        }
    }
}

print(str(query))
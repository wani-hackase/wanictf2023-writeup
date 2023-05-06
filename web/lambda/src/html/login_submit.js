window.onload = (event) => {
  const btn = document.querySelector("#submitBtn");

  btn.addEventListener("click", async () => {
    console.log("aaa");
    const password = document.querySelector(".password");
    const username = document.querySelector(".username");
    const result = document.querySelector(".result");
    console.log(password);
    console.log(username);
    const url = new URL(
      "https://k0gh2dp2jg.execute-api.ap-northeast-1.amazonaws.com/test/"
    );
    url.searchParams.append("PassWord", password.value);
    url.searchParams.append("UserName", username.value);
    const response = await fetch(url.href, { method: "get" });
    Promise.resolve(response.text()).then(
      (value) => {
        console.log(value);
        result.innerText = value;
      },
      (value) => {
        console.error(value);
      }
    );
  });
};

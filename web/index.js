const fileHandler = async (f) => {
    return new Promise((res) => {
        var reader = new FileReader();
        reader.onload = (e) => {
          // retrieved the base 64 image, you can't write using plain js 
          // console.log(e.target.result.split(",")[1]);
          img.src = e.target.result;
          res(e.target.result.split(",")[1]);
        };
        
        reader.readAsDataURL(f);
    });
  };

var img = document.getElementById("img");
var file_input = document.getElementById("up_file");
var up_cont = document.getElementById("up_container");
var loader = document.getElementById("loader");

file_input.addEventListener("change",async ()=>{
  // here I get the data
  // up_cont.setAttribute("hidden");
  loader.removeAttribute("hidden");
  const img64 = await fileHandler(file_input.files[0]);
  await eel.upscale_image(img64,file_input.files[0].name)
  loader.setAttribute("hidden",true);
  img.src = "./out/"+file_input.files[0].name+".jpg";
  // up_cont.removeAttribute("hidden");
})
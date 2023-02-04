const BASE_URL = "http://127.0.0.1:5000/api";

// Generate HTML for a cupcake
function createCupcakeHtml(cupcake) {
  return `
    <div data-cupcake-id="${cupcake.id}" class =' d-inline-flex m-1'>
    <img class='img-thumbnail w-50' src='${cupcake.image}' alt='(no image provided)'>
        <li class='d-block m-3'>
            ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
            <button class='delete-cupcake btn btn-success'>Delete</button>
        </li>
        
    </div>
    `;
}

// Display all the cupcakes
async function displayCupcakes() {
  response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcake of response.data.cupcakes) {
    let cupcakeData = $(createCupcakeHtml(cupcake));
    $("#cupcakes-list").append(cupcakeData);
  }
}

// Handle add new cupcake form
$("#new-cupcake-form").on("submit", async function addNewCupcake(e) {
  e.preventdefault();
  let flavor = $("#form-flavor").val();
  let size = $("#form-size").val();
  let rating = $("#form-rating").val();
  let image = $("#form-image").val();

  const response = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    size,
    rating,
    image,
  });
  let newCupcake = $(createCupcakeHtml(response.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});

// Handle delete button on each cupcake
$("#cupcakes-list").on("click", ".delete-cupcake", async function (evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

displayCupcakes();

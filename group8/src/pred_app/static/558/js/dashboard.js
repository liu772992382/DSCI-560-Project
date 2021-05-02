/* globals Chart:false, feather:false */

// cards container
let cardContainer;

var num_col = 2;

var host_name = "http://localhost:5000";


let createTaskCard = (task, deck_node, index) => {

  let card = document.createElement('div');
  card.className = 'card mb-3';
  card.style = 'max-width: 540px;';
  console.log(task.award);

  card.innerHTML += `<div class="row no-gutters">
    <div class="col-md-4">
      <img src="${task.gr_img_url}" class="card-img" alt="...">
    </div>
    <div class="col-md-8">
      <div class="card-body">
        <h5 class="card-title">
          ${task.title}
          ${task.gr_url ? `<a class="badge badge-warning" target="_blank" rel="558 proj" href="` + task.gr_url + `">G</a>` : ``}
          ${task.lbt_url ? `<a class="badge badge-info" target="_blank" rel="558 proj" href="` + task.lbt_url + `">L</a><br/>` : ``}
        </h5>
        <h6>by  
          <a data-toggle="modal" href="#" data-target="#staticBackdrop${index}">
          ${task.author}
          </a>

        </h6>
        

        <!-- Vertically centered scrollable modal -->
        <div class="modal" tabindex="-1" id="staticBackdrop${index}">
          <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Author Detail</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">


              <div class="card mb-3" style="max-width: 540px;">
                      <div class="row no-gutters">
                        <div class="col-md-4">
                          <img src="${task.aut_img_url}" class="card-img" alt="...">
                        </div>
                        <div class="col-md-8">
                          <div class="card-body">
                            <h5 class="card-title">${task.author} </h5>
                            <p class="card-text">
                              <b>Born:</b> ${task.birth_date}<br/>
                              <b>Gender:</b> ${task.gender}<br/>
                              <b>Nationality:</b> ${task.nationality} <br/>
                              <b>Education:</b> ${task.edus} <br/>
                              <b>Awards:</b> ${task.aut_awards} <br/>
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
              </div>
            </div>
          </div>
        </div>

          <p class="card-text">
          <b>Rating:</b> ${task.rating}   <b>Reviews:</b> ${task.reviews} <br/>
          <b>Public Date:</b> ${task.pbdate}<br/>
            ${task.award ? `<b>Award:</b> `+ task.award:``} <br/>
            ${task.movie ? `<b>Related movie:</b> <a target="_blank" rel="558 proj" href="`+task.mv_url +`">` + task.movie + `</a>` : ``}
            <div style="display:inline;">
              <span id="desc-${index}" data-desc="${task.description}" style="display:inline;">
                ${task.description.slice(0,100)} 
              </span>
              <a style="display:inline;" href="#/" id="more-${index}" data-flag="0" \
              onclick="swapContent(${index});">...more</a>
            </div>
        </div>
    </div>
  </div>`;

  deck_node.appendChild(card);
  $(function () {
    // console.log('pop');
    $('[data-toggle="popover"]').popover()
  })
}

let set_card_container = (results) => {
  console.log(results);
  cardContainer = document.getElementById('card-container');
  cardContainer.innerHTML = ""
  let l_res = results.length;
  console.log(l_res);
  for (i=0; i < results.length; i++){
    if (i % 2 == 0){
      var deck_node = document.createElement('div');
      deck_node.className = 'card-deck';
      cardContainer.appendChild(deck_node);
    }
    createTaskCard(results[i], deck_node, i);
  };
}

let search_request = (params) => {
  $.get(host_name + '/search', params, function (data) {
    // console.log(data[0]);
    set_card_container(JSON.parse(data));
  });
}
var params_2 = {}
let search_action = () => {
  params_2={}
  let search_content = document.getElementById('search_input').value;

  // console.log(search_content);
  if (!search_content){
    console.log('empty search content!');
    return;
  }

  // get request
  params_2['content']=search_content;
  // console.log(params_2)
  var params = {
    'content': search_content,
  };
//  console.log(params)
  search_request(params_2);
};

let apply_action = () =>{
    let params_2 = {
      'content' : document.getElementById('search_input').value,
      'author' : document.getElementById('author_input').value,
      'rating_content_1' : document.getElementById('rating_input_1').value,
      'rating_content_2' : document.getElementById('rating_input_2').value,
      'reviews_content_1' : document.getElementById('reviews_input_1').value,
      'reviews_content_2' : document.getElementById('reviews_input_2').value,
      'pbstart' : document.getElementById('pb_start').value,
      'pbend' : document.getElementById('pb_end').value,
      'order_by': document.getElementById('order_by').value,
      'desc': document.getElementById('descending').checked ? true: false,
    };
    // params_2['author'] = author_content;
    // if(rating_content_1)
    // {params_2['rating_lower'] = rating_content_1, 'upper': rating_content_2}}
    // if(reviews_content_1)
    // {params_2['reviews'] = {'lower': reviews_content_1, 'upper': reviews_content_2}}
    // if(pb_content_start)
    // {params_2['pbstart'] = pb_content_start}
    // if(pb_content_end)
    // {params_2['pbend'] = pb_content_end}
    // console.log(params_2)
    search_request(params_2);

}

let clear_content = () =>{
  cardContainer = document.getElementById('card-container');
  cardContainer.innerHTML = ""

  
  let author_content=document.getElementById('author_input');
  author_content.value = '';
  let rating_content_1=document.getElementById('rating_input_1');
  rating_content_1.value = '';
  let rating_content_2=document.getElementById('rating_input_2');
  rating_content_2.value = '';
  let reviews_content_1=document.getElementById('reviews_input_1');
  reviews_content_1.value = '';
  let reviews_content_2=document.getElementById('reviews_input_2');
  reviews_content_2.value = '';
  let pb_content_start=document.getElementById('pb_start');
  pb_content_start.value = '';
  let pb_content_end=document.getElementById('pb_end');
  pb_content_end.value = '';
}

// init result
$(document).ready(function() {
  params = {'content': 'Harry'};
  search_request(params);
});


let swapContent = (index) => {
  // let item = item[0];
  let item = document.getElementById('more-' + index);
  let prev = document.getElementById('desc-' + index);
  if (item.dataset.flag == "0"){
    prev.textContent = prev.dataset.desc;
    item.textContent = '(less)';
    item.dataset.flag = "1" ;
  }else{
    prev.textContent = prev.dataset.desc.slice(0, 100);
    item.textContent = '...more';
    item.dataset.flag = "0" ;
  }
}
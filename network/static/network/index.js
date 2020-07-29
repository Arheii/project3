document.addEventListener('DOMContentLoaded', function() {

  // send like to serve and update
  document.querySelectorAll('.likes').forEach(link => {
                    link.onclick = () => {
                        // Replace glyph icon and update value likes
                        if (link.className == "btn btn-default fa fa-heart-o likes") {
                          link.className = "btn btn-default fa fa-heart likes";
                          document.querySelector(`#likes_for_${link.dataset.id}`).innerHTML ++;
                        }
                        else {
                          link.className = "btn btn-default fa fa-heart-o likes";
                          document.querySelector(`#likes_for_${link.dataset.id}`).innerHTML --;
                        }

                        // Send update like request to servere
                        fetch(`/tweet/${link.dataset.id}`)
                          .then(response => {
                            console.log(response);
                          });
                    };
                });
  // if (document.querySelector('#follow')) {
  //   button = (document.querySelector('#follow');
  //   var user_id  = button.getAttribute('data-cmd');
  //   console.log('create follow button');
  //   folow = document.createElement('button');
  //   folow.id = 'folow';
  //   folow.className = "btn btn-sm btn-success m-2";
  //   folow.innerHTML = 'Follow';
  //   folow.addEventListener('click', () => {
  //     console.log(user_id);
  //   });
  //   document.querySelector('#follows_block').append(folow);
  //         ul.append(element);
});

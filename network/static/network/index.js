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
          fetch(`/tweet/${link.dataset.id}/like`)
            .then(response => {
              console.log(response);
            });
      };
  });

  // disabled text tweet and show form with textarea for editing
  document.querySelectorAll('.edit').forEach(button => {
      button.onclick = () => {
        document.querySelector(`#text_${button.dataset.id}`).style.display = 'none';
        document.querySelector(`#form_${button.dataset.id}`).style.display = 'block';
      };
  });

  // send update tweet request
  document.querySelectorAll('.tweet_form').forEach(form => {
      form.onsubmit = () => {

        const tweet_body = document.querySelector(`#textarea_${form.dataset.id}`).innerHTML;
        console.log(`send_form_request. new tweet text:\n ${tweet_body}`);

        fetch(`/tweet/${form.dataset.id}/edit`, {
          method: 'POST',
          body: JSON.stringify({
            'text': tweet_body
          })
        })
        .then(response => response.json())
        .then(result => {
            // if put finished correctly
            // if (result.status):
            console.log(result);
        });

        document.querySelector(`#text_${form.dataset.id}`).style.display = 'block';
        document.querySelector(`#form_${form.dataset.id}`).style.display = 'none';

        false; // stop reload page
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

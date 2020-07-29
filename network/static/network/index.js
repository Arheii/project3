document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll('.likes').forEach(link => {
      link.onclick = () => {

          // Send update like request to server via get
          fetch(`/tweet/${link.dataset.id}/like`)
            .then(response => {
              console.log(response);

              // sucsess
              if (response.status == 204) {

                // Replace glyph icon and update value likes
                if (link.className == "btn btn-default fa fa-heart-o likes") {
                  link.className = "btn btn-default fa fa-heart likes";
                  document.querySelector(`#likes_for_${link.dataset.id}`).innerHTML ++;
                }
                else {
                  link.className = "btn btn-default fa fa-heart-o likes";
                  document.querySelector(`#likes_for_${link.dataset.id}`).innerHTML --;
                }
              }
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

        const tweet_body = document.querySelector(`#textarea_${form.dataset.id}`).value;
        const csrftoken = document.querySelector(`#form_${form.dataset.id}`)[0].value;

        // send request with new text and scrf token
        fetch(`/tweet/${form.dataset.id}/edit`, {
          method: 'PUT',
          headers: {'X-CSRFToken': csrftoken},
          body: JSON.stringify({
            text: tweet_body
          })
        })
        .then(response => response.json())
        .then(result => {
              console.log(result);

              // request is sucsess
              if (result.new_text) {

                // replace tweet text for the new one
                document.querySelector(`#text_${form.dataset.id}`).children[0].innerHTML = result.new_text

                // switch form to plaint text
                document.querySelector(`#text_${form.dataset.id}`).style.display = 'block';
                document.querySelector(`#form_${form.dataset.id}`).style.display = 'none';
              }
          });

        return false; // stop reload page
      };
  });
});

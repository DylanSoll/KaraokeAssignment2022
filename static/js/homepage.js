hello_results = {"tracks":{
    'items':[
        {
            'data':{
                'id':'2r6OAV3WsYtXuXjvJ1lIDi', 'name':"Hello (feat. A Boogie Wit da Hoodie)", "albumOfTrack":{
                    "uri":"spotify:album:2MDU46hcBn3u94s46BOSdv","name":"Shoot For The Stars Aim For The Moon (Deluxe)","coverArt":{"sources":[{"url":"https:\/\/i.scdn.co\/image\/ab67616d00001e0246e1307c35579c3483ea7b03","width":300,"height":300},{"url":"https:\/\/i.scdn.co\/image\/ab67616d0000485146e1307c35579c3483ea7b03","width":64,"height":64},{"url":"https:\/\/i.scdn.co\/image\/ab67616d0000b27346e1307c35579c3483ea7b03","width":640,"height":640}]},"id":"2MDU46hcBn3u94s46BOSdv","sharingInfo":{"shareUrl":"https:\/\/open.spotify.com\/album\/2MDU46hcBn3u94s46BOSdv?si=jyVySdq3T8iyNttvyCICUA"}
                }, "artists":{"items":[{"uri":"spotify:artist:0eDvMgVFoNV3TpwtrVCoTj","profile":{"name":"Pop Smoke"}},{"uri":"spotify:artist:31W5EY0aAly4Qieq6OFu6I","profile":{"name":"A Boogie Wit da Hoodie"}}]}
            }
        }
    ]
}}


function create_search_result_item(data){
    console.table(data)
    const container = document.createElement('div');
    container.id = `track-${data.track_id}`;
    container.className = "search-result-item";

    const track_div = document.createElement('div');
    track_div.innerHTML = data.track_name;
    
    const album_art = document.createElement('img');
    
    album_art.src = data?.album_url;
    album_art.alt = `${data.album_name} Cover Art`;
    album_art.className = "album-art";

    const album_div = document.createElement('div');
    album_div.innerHTML = data.album_name;

    const artist_div = document.createElement('div');
    artist_div.innerHTML = data.artist_name;
    
    const preview_button = document.createElement('button');
    preview_button.innerHTML = 'Show Preview';
    preview_button.setAttribute('data-audio-id', data.track_id);
    preview_button.addEventListener('click', ()=>{
        audio_id = preview_button.getAttribute('data-audio-id');
        ajax_handler('/get-song', (results)=>{
            const audio_tag = document.createElement('audio')
            audio_tag.controls = true;
            audio_tag.autoplay = true;
            audio_tag.src = results.tracks[0].preview_url;
            document.getElementById(`track-${audio_id}`).appendChild(audio_tag)
        }, create_form_data({'track_id':audio_id}))
    })
    container.appendChild(track_div);
    container.appendChild(album_art);
    container.appendChild(album_div);
    container.appendChild(artist_div);
    container.appendChild(preview_button)
    console.log(container)
    return container
 }
 function search_results(results){
    document.getElementById('search_results').innerHTML = ""
    console.log(results.tracks)
    //only set to handle tracks
    const tracks_array = results.tracks.items;
    console.table(tracks_array)
    tracks_array.forEach(track => {
       let track_object = {};
       const track_data = track.data;
       const album_data = track_data.albumOfTrack; 
       console.table(track_data)
       console.table(album_data)
       track_object['track_name'] = track_data.name;
       track_object['track_id'] = track_data.id;
       track_object['artist_name'] = track_data.artists.items[0].profile.name;
       track_object['album_url'] = album_data?.coverArt?.sources[0]?.url;
       track_object['album_name'] = album_data?.name;
       document.getElementById('search_results').appendChild(create_search_result_item(track_object));
    });
 }

//search_results(hello_results)

function primary_search_button(){
    let form_data_input = {'query': document.getElementById('query').value};
    ajax_handler('/search-results', search_results, create_form_data(form_data_input));
}
document.getElementById('primary_search_button').addEventListener('click', primary_search_button)
% include('header.tpl', title='MTG Auction House')

<div class="container">
  <h1>{{ set_.get('name', 'Pas de set, pas de cartes.') }}</h1>
  <p class="lead">{{ rarity }}</p>
</div>
<div class="container">
  <div class="table-responsive">
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th>#</th>
          <th>rarity</th>
          <th>en</th>
          <th>fr</th>
          <th>type</th>
          <th>cost</th>
          <th>stats</th>
        </tr>
      </thead>
      <tbody>
        % for card in set_.get('cards', []): 
        <tr>
          <td>{{ card['number'] }}</td>
          <td>{{ card['rarity'][0]  }}</td>
          <td>
            <span>
              {{ card['name'] }}
              <img class="card" src="/static/img/{{ set_['code'] }}/{{ card['image_name'] }}.jpg"/>
            </span>
          </td>
          <td>{{ card['name'] }}</td>
          <td>{{ card['type'] }}</td>
          <td>
            % for cost_class in card.get('mana_cost', []):
              <span class="{{ cost_class }}"></span>
            % end
          </td>
          <td>
            % if card.get('power', False) and card.get('toughness', False):
              {{ card['power'] }}/{{ card['toughness'] }}
            % end
          </td> 
        </tr>
        % end
      </tbody>
    </table>
  </div>
</div>

% include('footer.tpl', available_sets=available_sets)

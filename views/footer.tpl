    <div id="footer">
      <div class="container">
        % for set_ in available_sets:
          <a href="/{{ set_ }}">
            <span class="label label-primary">{{ set_ }}</span>
          </a>
        % end
      </div>
    </div>
  </body>
</html>

package ws.donmez.burulas;

import java.util.ArrayList;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;

public class BackwardStopsActivity extends ListActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setListAdapter(new ArrayAdapter<String>(this,
                                        android.R.layout.simple_list_item_1,
                                        this.getBackwardRoute()));
    }

    private ArrayList<String> getBackwardRoute() {
        Intent intent = getIntent();
        return intent.getStringArrayListExtra("BackwardStops");
    }
}


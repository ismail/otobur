package ws.donmez.burulas;

import android.app.ActionBar;
import android.app.ActionBar.OnNavigationListener;
import android.app.Fragment;
import android.app.FragmentManager;
import android.os.Bundle;
import android.support.v13.app.FragmentStatePagerAdapter;
import android.support.v4.app.FragmentActivity;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v4.view.ViewPager.OnPageChangeListener;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.SpinnerAdapter;

public class DetailsSlideActivity extends FragmentActivity {

    private ViewPager mPager;
    private PagerAdapter mPagerAdapter;
    private SpinnerAdapter mSpinnerAdapter;
    private OnNavigationListener mOnNavigationListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_screen_slide);

        // Instantiate a ViewPager and a PagerAdapter.
        mPager = (ViewPager) findViewById(R.id.pager);
        mPagerAdapter = new DetailsSlidePagerAdapter(getFragmentManager());
        mPager.setAdapter(mPagerAdapter);

        mSpinnerAdapter = ArrayAdapter.createFromResource(this, R.array.action_list,
                                                          android.R.layout.simple_spinner_dropdown_item);

        mOnNavigationListener = new OnNavigationListener() {
            String[] strings = getResources().getStringArray(R.array.action_list);

            @Override
            public boolean onNavigationItemSelected(int position, long itemId) {
                mPager.setCurrentItem(position);
                return true;
            }
        };

        mPager.setOnPageChangeListener(new OnPageChangeListener() {

            @Override
            public void onPageSelected (int position) {
                if (position > 2)
                    position = 2;
                getActionBar().setSelectedNavigationItem(position);
            }

            @Override
            public void onPageScrolled(int arg0, float arg1, int arg2) {}

            @Override
            public void onPageScrollStateChanged(int arg0) {}

        });

        ActionBar actionBar = getActionBar();
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_LIST);
        actionBar.setListNavigationCallbacks(mSpinnerAdapter, mOnNavigationListener);
        actionBar.setTitle(MainActivity.currentBus.name);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.activity_details_slide, menu);
        return true;
    }

    private class DetailsSlidePagerAdapter extends FragmentStatePagerAdapter {
        public DetailsSlidePagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
            return DetailsSlidePageFragment.create(position);
        }

        @Override
        public int getCount() {
            int hourCount = MainActivity.currentBus.hours.size();
            return hourCount+2;
        }
    }
}
